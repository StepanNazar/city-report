import React from 'react';

const PostOpen = ({ post }) => {
  return (
    <div className='post'>
      <div className="post__content">
        <h3>{post.id}. {post.title}</h3>
        <p><strong>Автор ID:</strong> {post.authorId}</p>
        <p><strong>Ім'я автора:</strong> {post.authorName}</p>
        <p><strong>Дата створення:</strong> {post.createdAt}</p>
        <p><strong>Координати:</strong> {post.latitude}, {post.longitude}</p>
        <p><strong>Країна:</strong> {post.country}</p>
        <p><strong>Область:</strong> {post.state}</p>
        <p><strong>Населений пункт:</strong> {post.locality}</p>
        <p><strong>Опис:</strong> {post.body}</p>
      </div>
    </div>
  );
};

export default PostOpen;
