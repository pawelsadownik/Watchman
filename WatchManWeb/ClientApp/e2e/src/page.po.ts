import { browser, element, by } from "protractor";

export abstract class Page {
  HomePage = require("./home.po").HomePage;
  LoginPage = require("./login.po").LoginPage;
  MonitoringPage = require("./monitoring.po").MonitoringPage;
  AnalysisPage = require("./analysis.po").AnalysisPage;
  ReportsPage = require("./reports.po").ReportsPage;
  UsersPage = require("./users.po").UsersPage;
  
  homeUrl = '/';
  loginUrl = '/login';
  monitoringUrl = '/monitoring';
  analysisUrl = '/analysis';
  reportsUrl = '/reports';
  usersUrl = '/users/list';
  userDetailsUrl = '/users/details';

  navHome = element(by.css(`#main-nav a[href='${this.homeUrl}'`));
  navLogin = element(by.css(`#main-nav a[href='${this.loginUrl}'`));
  navMonitoring = element(by.css(`#main-nav a[href='${this.monitoringUrl}'`));
  navAnalysis = element(by.css(`#main-nav a[href='${this.analysisUrl}'`));
  navReports = element(by.css(`#main-nav a[href='${this.reportsUrl}'`));
  navUsers = element(by.css(`#main-nav a[href='${this.usersUrl}'`));

  btnLogout = element(by.id("btn-logout"));
  currentUser = element(by.id("current-user"));

  testFirstName = 'Test';
  
  getCurrentUser() {
    return this.currentUser;
}

  goToHomePage() :any {
      this.navHome.click();
      return new this.HomePage();
  }

  goToLoginPage() :any {
      this.navLogin.click();
      return new this.LoginPage();
  }

  goToMonitoringPage() :any {
      this.navMonitoring.click();
      return new this.MonitoringPage();
  }

  goToAnalysisPage() :any {
      this.navAnalysis.click();
      return new this.AnalysisPage();
  }

  goToReportsPage() :any {
      this.navReports.click();
      return new this.ReportsPage();
  }

  goToUsersPage() :any {
      this.navUsers.click();
      return new this.UsersPage();
  }

  logOut() :any {
    this.btnLogout.click();
    return new this.LoginPage();
  }

  clearStorage() {
    browser.executeScript('window.sessionStorage.clear();');
    browser.executeScript('window.localStorage.clear();');
  }
}