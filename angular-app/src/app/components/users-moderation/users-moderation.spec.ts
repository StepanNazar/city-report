import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsersModeration } from './users-moderation';

describe('UsersModeration', () => {
  let component: UsersModeration;
  let fixture: ComponentFixture<UsersModeration>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UsersModeration]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UsersModeration);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
