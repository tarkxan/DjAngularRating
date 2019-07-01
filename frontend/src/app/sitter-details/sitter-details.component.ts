import { Component, OnInit, Input } from '@angular/core';
import { SitterService } from '../sitter.service';
import { Sitter } from '../sitter';

import { SittersListComponent } from '../sitters-list/sitters-list.component';

@Component({
  selector: 'app-sitter-details',
  templateUrl: './sitter-details.component.html',
  styleUrls: ['./sitter-details.component.css']
})
export class SitterDetailsComponent implements OnInit {

  @Input() sitter: Sitter;

  constructor(private sitterService: SitterService,
              private listComponent: SittersListComponent) { }

  ngOnInit() {
  }

}
