import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PasswordPanel } from './password-panel';

describe('PasswordPanel', () => {
  let component: PasswordPanel;
  let fixture: ComponentFixture<PasswordPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PasswordPanel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PasswordPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
