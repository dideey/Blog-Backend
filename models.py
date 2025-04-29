from sqlalchemy.orm import declarative_base, relationship # Updated import
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Unicode

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    author = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    reactions = relationship("PostReaction", back_populates="post", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<BlogPost(title='{self.title}', author={self.author})>"

class PostReaction(Base):
    __tablename__ = "post_reactions"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("blog_posts.id", ondelete="CASCADE"))
    reaction_type = Column(Unicode, nullable=False)  # Unicode supports emojis
    count = Column(Integer, default=1)

    post = relationship("BlogPost", back_populates="reactions")