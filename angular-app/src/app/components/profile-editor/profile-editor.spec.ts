import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileEditor } from './profile-editor';

describe('ProfileEditor', () => {
  let component: ProfileEditor;
  let fixture: ComponentFixture<ProfileEditor>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProfileEditor]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProfileEditor);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
