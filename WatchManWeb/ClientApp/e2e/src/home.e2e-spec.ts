import { HomePage } from './home.po';
import { LoginPage } from './login.po';
import { browser } from 'protractor';

describe('Home Page - Public', () => {

    let homePage: HomePage;

    beforeEach(() => {
        homePage = new HomePage().get();
    });

    it('should display title', () => {
        homePage.get();
        expect(browser.getTitle()).toEqual('WATCHMAN');
      });

    it('should not display current user', () => {
        expect(homePage.getCurrentUser().isPresent()).toBe(false);
    });

    it('should allow to reach login page', () => {
        let loginPage = homePage.goToLoginPage();
        expect(loginPage.get().getLoginForm().isPresent()).toBe(true);
    });
});



