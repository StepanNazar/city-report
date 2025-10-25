import { Component, signal } from '@angular/core';
import { UserHeader } from '../../components/user-header/user-header';
import { PostsList } from '../../components/posts-list/posts-list';
import { SolutionsList } from '../../components/solutions-list/solutions-list';
import { CommentsList } from '../../components/comments-list/comments-list';
import { PublicStats } from '../../components/public-stats/public-stats';

@Component({
  selector: 'app-user-page',
  imports: [UserHeader, PostsList, SolutionsList, CommentsList, PublicStats],
  templateUrl: './user-page.html',
  styleUrl: './user-page.scss'
})
export class UserPage {
  activeTab = signal<'posts' | 'solutions' | 'comments'>('posts');
}
