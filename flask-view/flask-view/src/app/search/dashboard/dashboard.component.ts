import {Component, OnInit, ViewChild, ElementRef , SimpleChanges, Directive, Input, OnChanges} from '@angular/core';
import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';
import {Result} from '../../Model/result';
import {ProductServiceService} from '../../Service/ProductService.service';
import {TwitterResult} from '../../Model/twitterresult';
import * as Highcharts from 'highcharts';
import {NotificationService} from '../../Service/notification.service';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  // tslint:disable-next-line:ban-types
  step = 0;
  constructor(private productService: ProductServiceService, private notificationService: NotificationService) { }
  ngOnInit() {
    this.notificationService.success(':: Search Engine successfully');
  }

  setStep(index: number) {
    this.step = index;
  }

  nextStep() {
    this.step++;
  }

  prevStep() {
    this.step--;
  }
}
