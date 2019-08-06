import { Component, OnInit } from '@angular/core';
import {Product} from '../Model/product';
import {ProductServiceService} from '../Service/ProductService.service';

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.css']
})
export class ProductsComponent implements OnInit {

  proList: Product[];
  constructor(private productService: ProductServiceService) { }

  ngOnInit() {
    this.productService.getProducts().subscribe(
      res => {
        this.proList = res;
      },
      error1 => {
        alert('Error come!!!');
      }
    );
  }

}
