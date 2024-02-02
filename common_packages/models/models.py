from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, Text, String, BigInteger

db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = 'customers'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # This should be hashed and salted

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }


class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = Column(BigInteger, primary_key=True)
    customer_id = Column(BigInteger, ForeignKey('customers.id'))
    active = Column(Boolean, nullable=False)
    private_key = Column(Text, nullable=False)
    certificate_body = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'active': self.active,
            'private_key': self.private_key,
            'certificate_body': self.certificate_body
        }
