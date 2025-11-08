import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditOptions } from './edit-options';

describe('EditOptions', () => {
  let component: EditOptions;
  let fixture: ComponentFixture<EditOptions>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditOptions]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditOptions);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
