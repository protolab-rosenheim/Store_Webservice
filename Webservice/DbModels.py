from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DbModelExtension(db.Model):
    __abstract__ = True

    def to_dict(self):
        tmp_dict = self.__dict__
        ret_dict = {}
        for key in self.__table__.columns.keys():
            if key in tmp_dict:
                if tmp_dict[key].__class__.__name__ == 'datetime':
                    ret_dict[key] = tmp_dict[key].isoformat()
                else:
                    ret_dict[key] = tmp_dict[key]
        return ret_dict

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.to_dict() == other.to_dict():
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


# TODO: OptiMatParam, OptiBoardParam??
class Board(DbModelExtension):
    Identnummer = db.Column(db.Unicode, primary_key=True)
    Material = db.Column(db.Unicode)
    Dekor = db.Column(db.Unicode)
    Laenge = db.Column(db.Integer)
    Breite = db.Column(db.Integer)
    Dicke = db.Column(db.Integer)
    Maserung = db.Column(db.Integer)
    Kosten = db.Column(db.Numeric)
    BestandPhys = db.Column(db.Integer)
    Geplant = db.Column(db.Integer)
    Barcode = db.Column(db.Unicode)
    MaxPaketHoehe = db.Column(db.Integer)
    MinBestand = db.Column(db.Integer)
    OptiMatParam = db.Column(db.Unicode)
    OptiBoardParam = db.Column(db.Unicode)
    OptiFunctionCode = db.Column(db.Integer)
