from datetime import datetime

from flask import abort
from flask_restful import Resource
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

from ..security import auth_token_required, encrypt_password
from ..parsers import create_user_parser
from ..model import PostgresSession
from ..model.pharmacy_user import PharmacyUser

class PharmacyUserResource(Resource):

    def _get_user(self, user_id):
        session = PostgresSession()

        user = session.query(PharmacyUser). \
            select_from(PharmacyUser).\
            filter(PharmacyUser._id == user_id).one_or_none()

        return user

    def _inactive_user(self, user_id):
        user = self._get_user(user_id)
        session = PostgresSession()

        if not user:
            abort(404, 'User not found')
        
        session.query(PharmacyUser) \
        .filter(PharmacyUser._id == user_id) \
        .update({
            PharmacyUser.is_active: not user.is_active
        })
        session.commit()
        return user

    def _create_user(self, informations):
        password = encrypt_password(informations.password)
        user = PharmacyUser(
            username=informations.username,
            password=password,
            creation_date=datetime.now(),
            is_admin=informations.is_admin)

        try:
            session = PostgresSession()
            session.add(user)
            session.commit()
        except IntegrityError:
            abort(400, 'Username already exist')
        finally:
            session.close()
        
        return user

    @auth_token_required()
    def get(self, user_id):
        user = self._get_user(user_id)
        informations = {
            'id': user._id,
            'username': user.username,
            'is_active': user.is_active,
            'creation_date': str(user.creation_date)
        }
        return informations, 200

    @auth_token_required()
    def post(self):
        args = create_user_parser.parse_args()

        if args.is_admin and not self.user_info['is_admin']:
            abort(403, "You do not have permisson to create Admin's user")
        
        self._create_user(args)
        return {'message': f'User {args.username} was created successfuly'}, 201

    @auth_token_required(only_admin=True)
    def patch(self, user_id):
        user = self._inactive_user(user_id)
        action = 'activated' if user.is_active else 'inactivated'
        return {'message': f'User {user.username} {action}'}, 200

class PharmacyUsersResource(Resource):

    def _get_users(self):
        session = PostgresSession()
        users = session.query(
            PharmacyUser._id.label('id'),
            PharmacyUser.username,
            PharmacyUser.is_active,
            func.to_char(
                PharmacyUser.creation_date, 'YYYY-MM-DD HH:MM:SS')
                    .label('creation_date')) \
            .all()
        return [u._asdict() for u in users]

    @auth_token_required(only_admin=True)
    def get(self):
        return self._get_users()
