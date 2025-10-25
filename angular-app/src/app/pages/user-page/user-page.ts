import {Component, inject} from '@angular/core';
import {ActivatedRoute, RouterLink, Router} from '@angular/router';
import { UserHeader } from '../../components/user-header/user-header';
import { PublicStats } from '../../components/public-stats/public-stats';
import {PostsList} from '../../components/posts-list/posts-list';
import {CommentsList} from '../../components/comments-list/comments-list';
import {SolutionsList} from '../../components/solutions-list/solutions-list';

@Component({
  selector: 'app-user-page',
  imports: [UserHeader, PublicStats, PostsList, CommentsList, SolutionsList],
  templateUrl: './user-page.html',
  styleUrl: './user-page.scss'
})
export class UserPage {
  currentTab = 'posts';
  router = inject(Router);
  route = inject(ActivatedRoute);

  constructor() {
    this.route.queryParamMap.subscribe(params => {
      this.currentTab = params.get('tab') ?? 'posts';
    });
  }

  switchTab(tab: string) {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { tab },
      queryParamsHandling: 'merge',
    });
  }
}
