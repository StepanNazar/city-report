import { Component } from '@angular/core';
import { ReactionPanel } from '../reaction-panel/reaction-panel';
import { Comment } from '../comment/comment';

@Component({
  selector: 'app-solution',
  imports: [ReactionPanel, Comment],
  templateUrl: './solution.html',
  styleUrl: './solution.scss'
})
export class Solution {

}
