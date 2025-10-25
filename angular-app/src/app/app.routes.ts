import { Routes } from '@angular/router';
import { Homepage } from './pages/homepage/homepage';
import { AuthPage } from './pages/auth-page/auth-page';
import { CreatePostPage } from './pages/create-post-page/create-post-page';
import { PostPage } from './pages/post-page/post-page';
import { AccountSettingsPage } from './pages/account-settings-page/account-settings-page';
import { LocationsPage } from './pages/locations-page/locations-page';
import { AdminPage } from './pages/admin-page/admin-page';
import { UserPage } from './pages/user-page/user-page';

export const routes: Routes = [
  { path: '', component: Homepage },
  { path: 'auth', component: AuthPage },
  { path: 'create-post', component: CreatePostPage },
  { path: 'post/:id', component: PostPage },
  { path: 'account-settings', component: AccountSettingsPage },
  { path: 'locations', component: LocationsPage },
  { path: 'admin', component: AdminPage },
  { path: 'user/:id', component: UserPage },
  { path: '**', redirectTo: '' }
];
