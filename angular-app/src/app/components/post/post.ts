import { Component } from '@angular/core';
import { ReactionPanel } from '../reaction-panel/reaction-panel';
import { EditOptions } from '../edit-options/edit-options';

@Component({
  selector: 'app-post',
  imports: [ReactionPanel, EditOptions],
  templateUrl: './post.html',
  styleUrl: './post.scss'
})
export class Post {

}
