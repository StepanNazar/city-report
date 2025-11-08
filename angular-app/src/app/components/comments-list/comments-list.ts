import { Component } from '@angular/core';
import { Comment } from '../comment/comment';

@Component({
  selector: 'app-comments-list',
  imports: [Comment],
  templateUrl: './comments-list.html',
  styleUrl: './comments-list.scss'
})
export class CommentsList {

}
