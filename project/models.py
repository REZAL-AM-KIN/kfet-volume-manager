from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    dn = db.Column(db.String(255), unique=True)

    # La chaine de texte suivante va servir à stocker les groupes de l'utilisateur séparer par des ;
    # Ce n'est pas la meilleure manière de stocker une liste dans une base de donnée
    # Mais comme cette liste n'est pas amené à être manipulée (à part en lecture)
    # La solution est suffisante.
    _memberships = db.Column(db.String, default='')

    @property
    def memberships(self):
        return self._memberships.split(';')

    @memberships.setter
    def memberships(self, value):
        self._memberships = ";".join(value)