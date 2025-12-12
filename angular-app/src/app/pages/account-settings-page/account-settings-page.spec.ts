import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountSettingsPage } from './account-settings-page';

describe('AccountSettingsPage', () => {
  let component: AccountSettingsPage;
  let fixture: ComponentFixture<AccountSettingsPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccountSettingsPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AccountSettingsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
