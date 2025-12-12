import { Component } from '@angular/core';
import { ReactionPanel } from '../reaction-panel/reaction-panel';

@Component({
  selector: 'app-comment',
  imports: [ReactionPanel],
  templateUrl: './comment.html',
  styleUrl: './comment.scss'
})
export class Comment {

}
