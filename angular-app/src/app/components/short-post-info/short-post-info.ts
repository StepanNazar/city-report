import { Component, input } from '@angular/core';
import { ReactionPanel } from '../reaction-panel/reaction-panel';
import { PostResponse } from '../../services/posts.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-short-post-info',
  imports: [ReactionPanel, DatePipe],
  templateUrl: './short-post-info.html',
  styleUrl: './short-post-info.scss'
})
export class ShortPostInfo {
  post = input.required<PostResponse>();
}
