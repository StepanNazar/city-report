import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminsList } from './admins-list';

describe('AdminsList', () => {
  let component: AdminsList;
  let fixture: ComponentFixture<AdminsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminsList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminsList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
