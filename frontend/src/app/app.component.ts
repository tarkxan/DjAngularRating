import { Component } from '@angular/core';
import { mapToMapExpression } from '@angular/compiler/src/render3/util';
import { SitterService } from './sitter.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [SitterService]
})
export class AppComponent {

  constructor() {
  }

}
