import { Routes } from '@angular/router';
import { Homepage } from './pages/homepage/homepage';
import { AuthPage } from './pages/auth-page/auth-page';
import { CreatePostPage } from './pages/create-post-page/create-post-page';
import { PostPage } from './pages/post-page/post-page';
import { AccountSettingsPage } from './pages/account-settings-page/account-settings-page';
import { LocationsPage } from './pages/locations-page/locations-page';
import { AdminPage } from './pages/admin-page/admin-page';
import { UserPage } from './pages/user-page/user-page';
import { SignInComponent } from './components/sign-in-component/sign-in-component';
import { SignUpComponent } from './components/sign-up-component/sign-up-component';

export const routes: Routes = [
  { path: '', component: Homepage, title: 'City Report Home' },
  {
    path: '',
    component: AuthPage,
    title: 'City Report Auth',
    children: [
      { path: 'signin', component: SignInComponent, title: 'Sign In' },
      { path: 'signup', component: SignUpComponent, title: 'Sign Up' }
    ]
  },
  { path: 'create-post', component: CreatePostPage, title: 'City Report Create Post' },
  { path: 'post/:id', component: PostPage, title: 'City Report Post' },
  { path: 'account-settings', component: AccountSettingsPage, title: 'City Report Settings' },
  { path: 'locations', component: LocationsPage, title: 'City Report Locations' },
  { path: 'admin', component: AdminPage, title: 'City Report Admin Panel' },
  { path: 'user/:id', component: UserPage, title: 'City Report User', },
  { path: '**', redirectTo: '' }
];
