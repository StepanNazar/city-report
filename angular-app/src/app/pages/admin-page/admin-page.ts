import { Component } from '@angular/core';
import { ReportsList } from '../../components/reports-list/reports-list';
import { ReportDetails } from '../../components/report-details/report-details';
import { AdminsList } from '../../components/admins-list/admins-list';
import { AIConfig } from '../../components/aiconfig/aiconfig';
import { UsersModeration } from '../../components/users-moderation/users-moderation';

@Component({
  selector: 'app-admin-page',
  imports: [ReportsList, ReportDetails, AdminsList, AIConfig, UsersModeration],
  templateUrl: './admin-page.html',
  styleUrl: './admin-page.scss'
})
export class AdminPage {

}
