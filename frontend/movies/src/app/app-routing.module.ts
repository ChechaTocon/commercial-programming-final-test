import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { CategoriaComponent } from './components/categoria/categoria.component'
import { CreateCategoryComponent } from './components/categoria/create-category/create-category.component'

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'category', component: CategoriaComponent },
  { path: 'category/:id', component: CreateCategoryComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled'
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
