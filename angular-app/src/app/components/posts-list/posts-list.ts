import { Component } from '@angular/core';
import { ShortPostInfo } from '../short-post-info/short-post-info';

@Component({
  selector: 'app-posts-list',
  imports: [ShortPostInfo],
  templateUrl: './posts-list.html',
  styleUrl: './posts-list.scss'
})
export class PostsList {

}
