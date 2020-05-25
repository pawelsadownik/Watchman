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

describe('Home Page - Admin', () => {

    let homePage: HomePage;

    beforeEach(() => {
        homePage = new LoginPage().get().doAdminLogin();
    });

    afterEach(() => {
        homePage.clearStorage();
    });

    it('should display admin as current user', () => {
        expect(homePage.getCurrentUser().getText()).toContain('admin');
    });

    it('should be able to go to monitoring', () => {
        homePage.goToMonitoringPage();
        expect(browser.getCurrentUrl()).toContain(homePage.monitoringUrl);
    });

    it('should be able to go to analysis', () => {
        homePage.goToAnalysisPage();
        expect(browser.getCurrentUrl()).toContain(homePage.analysisUrl);
    });

    it('should be able to go to reports', () => {
        homePage.goToReportsPage();
        expect(browser.getCurrentUrl()).toContain(homePage.reportsUrl);
    });
    
    it('should be able to go to users', () => {
        homePage.goToUsersPage();
        expect(browser.getCurrentUrl()).toContain(homePage.usersUrl);
    });

    it('should be able to logout', () => {
        homePage.logOut();
        expect(homePage.getCurrentUser().isPresent()).toBe(false);
    });
    
});

