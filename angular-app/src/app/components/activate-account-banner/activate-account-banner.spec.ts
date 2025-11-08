import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActivateAccountBanner } from './activate-account-banner';

describe('ActivateAccountBanner', () => {
  let component: ActivateAccountBanner;
  let fixture: ComponentFixture<ActivateAccountBanner>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ActivateAccountBanner]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ActivateAccountBanner);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
