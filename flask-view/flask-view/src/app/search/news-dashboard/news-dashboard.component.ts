import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {Result} from '../../Model/result';
import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';
import {ProductServiceService} from '../../Service/ProductService.service';
import {NotificationService} from '../../Service/notification.service';

@Component({
  selector: 'app-news-dashboard',
  templateUrl: './news-dashboard.component.html',
  styleUrls: ['./news-dashboard.component.css']
})
export class NewsDashboardComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  options: Object;
  displayedColumns: string[] = ['id', 'source', 'title' , 'score' ];
  result: Result[] = [];
  listResult: MatTableDataSource<any>;
  mode = 'determinate';
  average: number;
  constructor(private productService: ProductServiceService, private notificationService: NotificationService) { }

  ngOnInit() {
        this.productService.getDashboardResult().subscribe(
      res => {
        this.notificationService.success(':: Sentiment for news successfully');
        this.average = res.average;
        this.result = res.list;
        this.filterValueIntoMatSource(this.result);
        this.options = {
            title : { text : 'Sentiment distribution for News' },
            subtitle: {
                text: 'Source: '
            },
            chart: { type: 'column' ,
              width: 450,
              height: 300
            },
            xAxis: {
                categories: ['0-10', '10-20', '20-30', '30-40', '40-50'
                , '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'],
                title: {
                    text: 'Sentiment Score %'
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Density',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
             tooltip: {
                  valueSuffix: ' '
              },
             series: [{
                data: res.chartData
            }]
        };
      },
      error1 => {
        this.notificationService.warn(':: Error come from news');
      }
    );
  }
  filterValueIntoMatSource(results: Result[]) {
    this.listResult = new MatTableDataSource(results);
    this.listResult.sort = this.sort;
    this.listResult.paginator = this.paginator;
    this.listResult.filterPredicate =
      (data: Result, filter: string) => (data.id !== null) ? (data.score !== Number.parseFloat(filter)) : false;
  }
  redirectPage(element: Result) {
     window.open(element.url, '_blank');
  }
}
