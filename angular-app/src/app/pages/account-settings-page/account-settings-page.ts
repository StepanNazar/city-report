import { Component } from '@angular/core';
import { ProfileEditor } from '../../components/profile-editor/profile-editor';
import { PasswordPanel } from '../../components/password-panel/password-panel';
import { DevicesPanel } from '../../components/devices-panel/devices-panel';
import { ActivationPanel } from '../../components/activation-panel/activation-panel';

@Component({
  selector: 'app-account-settings-page',
  imports: [ProfileEditor, PasswordPanel, DevicesPanel, ActivationPanel],
  templateUrl: './account-settings-page.html',
  styleUrl: './account-settings-page.scss'
})
export class AccountSettingsPage {

}
