import { Component } from '@angular/core';
import { Comment } from '../comment/comment';

@Component({
  selector: 'app-comments',
  imports: [Comment],
  templateUrl: './comments.html',
  styleUrl: './comments.scss'
})
export class Comments {

}
