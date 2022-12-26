from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.exc import InvalidRequestError



db = SQLAlchemy()


class URL(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key = True)
    original_url = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    click = db.Column(db.Integer, default = 1)
    
    def __repr__(self) -> str:
        return f"<original_url: {self.original_url}, created_time: {self.created_time}, total_click: {self.click}>"
    
    @classmethod
    def get_all_datas(cls):
        datas = db.session.query(cls).all()
        return datas


    @classmethod
    def add_url(cls, original_url):
        new_url = URL(original_url=original_url)
        db.session.add(new_url)
        db.session.commit()
        
    
    def get_row(self, original_url):
        row = self.query.filter_by(original_url=original_url).first()
        return row
    
    def get_url_with_id(self, id):
        url = self.query.get(id)
        return url.original_url
    
    @classmethod
    def order_by(cls, object):
        cls.query.order_by(object).all()
    

        
    
    
    
        
    
        
        
        
    
    