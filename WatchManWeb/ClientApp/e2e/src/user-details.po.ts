import { browser, element, by } from "protractor";
import { Page } from "./page.po";
import { UsersPage } from "./users.po";

export class UserDetailsPage extends Page {

    private userForm = element(by.id("user-form"));

    private txtUsername = this.userForm.element(by.css("input[name='username']"));
    private txtFirstName = this.userForm.element(by.css("input[name='first-name']"));
    private txtPassword = this.userForm.element(by.css("input[name='password']"));
    private txtUserType = this.userForm.element(by.css("input[name='user-type']"));
    private btnSave = this.userForm.element(by.css("button[name='save'"));

    private createUser(username: string, firstName: string, password: string, userType: string,) :UsersPage{
        this.txtUsername.sendKeys(username);
        this.txtFirstName.sendKeys(firstName);
        this.txtPassword.sendKeys(password);
        this.txtUserType.sendKeys(password);
        this.btnSave.click();
        return new UsersPage();
    }

    get(): UserDetailsPage {
        browser.get(this.userDetailsUrl);
        return this;
    }

    getUserForm() {
        return this.userForm;
    }

    createTestUser() :UsersPage {
        this.createUser('test', this.testFirstName, '1234', 'BasicUser');
        return new UsersPage();
    }
}