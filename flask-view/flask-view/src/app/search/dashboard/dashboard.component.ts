import {Component, OnInit, ViewChild} from '@angular/core';
import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';
import {Result} from '../../Model/result';
import {ProductServiceService} from '../../Service/ProductService.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  step = 0;
  constructor(private productService: ProductServiceService) { }
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  displayedColumns: string[] = ['id', 'source', 'title' , 'score' ];
  result: Result[] = [];
  listResult: MatTableDataSource<any>;
  ngOnInit() {
    this.productService.getDashboardResult().subscribe(
      res => {
        this.result = res;
        this.filterValueIntoMatSource(this.result);
      },
      error1 => {
        alert('error');
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
