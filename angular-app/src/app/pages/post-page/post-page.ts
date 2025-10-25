import { Component } from '@angular/core';
import { Post } from '../../components/post/post';
import { AIComment } from '../../components/aicomment/aicomment';
import { Solutions } from '../../components/solutions/solutions';
import { Comments } from '../../components/comments/comments';

@Component({
  selector: 'app-post-page',
  imports: [Post, AIComment, Solutions, Comments],
  templateUrl: './post-page.html',
  styleUrl: './post-page.scss'
})
export class PostPage {

}
