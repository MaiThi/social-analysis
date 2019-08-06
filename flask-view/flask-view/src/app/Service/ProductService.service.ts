import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Product} from '../Model/Product';
import {Search} from '../Model/search';
import {Item} from '../Model/item';
import {Result} from '../Model/result';

@Injectable({
  providedIn: 'root'
})
export class ProductServiceService {

  private BASE_URL = 'http://localhost:5000/';
  private PRODUCT_URL = this.BASE_URL + 'products';
  private SAVE_UPDATE_LOCATION_URL = this.PRODUCT_URL;
  private SEARCH_URL = this.BASE_URL + 'search';

  constructor(private http: HttpClient) { }

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.PRODUCT_URL);
  }

  getProductById(id: number): Observable<Product> {
    return this.http.get<Product>(this.PRODUCT_URL + '/' + id);
  }

  getSearchsResult(keyword: string): Observable<Item> {
    return this.http.get<Item>(this.SEARCH_URL + '/' + keyword);
  }
  getDashboardResult(): Observable<Result[]> {
    return this.http.get<Result[]>(this.BASE_URL + 'analysic');
  }

  deleteAllResults(): Observable<any> {
    return this.http.get<any>(this.BASE_URL + 'searched/deleteAll');
  }
}
