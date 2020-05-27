import { browser, by, element } from "protractor";
import { HomePage } from "./home.po";
import { Page } from "./page.po"

export class LoginPage extends Page {
    
    private txtUsername = element(by.css("input[name='username']"));
    private txtPassword = element(by.css("input[name='password']"));
    private btnSignIn = element(by.css("button[name='login'"));
    private loginForm = element(by.id("login-form"));

    private logIn(username: string, password: string) :HomePage {
        this.txtUsername.sendKeys(username);
        this.txtPassword.sendKeys(password);
        this.btnSignIn.click();
        return new HomePage();
    }

    get(): LoginPage {
        browser.get(this.loginUrl);
        return this;
    }

    getLoginForm() {
        return this.loginForm;
    }

    doBasicLogin() :HomePage {
        return this.logIn('basic', '1234');
    }

    doAdvancedLogin() :HomePage {
        return this.logIn('advanced', '1234');
    }

    doAdminLogin() :HomePage {
        return this.logIn('admin', '1234');
    }
}