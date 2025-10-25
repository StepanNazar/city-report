import { Component, signal } from '@angular/core';
import { SignInComponent } from '../../components/sign-in-component/sign-in-component';
import { SignUpComponent } from '../../components/sign-up-component/sign-up-component';

@Component({
  selector: 'app-auth-page',
  imports: [SignInComponent, SignUpComponent],
  templateUrl: './auth-page.html',
  styleUrl: './auth-page.scss'
})
export class AuthPage {
  activeTab = signal<'signin' | 'signup'>('signin');
}
