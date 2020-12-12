import { Route } from '@angular/compiler/src/core';
import { Component, OnInit, DoCheck } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { from } from 'rxjs';
import { User } from 'src/app/models/user.model';
import { UserService} from '../../services/user.service'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  
  public cargando: boolean | undefined;
  public status: string | undefined;
  public identity: string | undefined;
  public user: User = new User();
  public token:string | undefined;
  public firstFormGroup: FormGroup | undefined;

  constructor(
    private _userService: UserService,
  ) {
    this.user = new User();
  }

  ngOnInit(): void {}

  Ingresar() {
  }
}
