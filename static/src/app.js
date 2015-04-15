'use-strict'

var thrum = angular.module('thrum', ['ui.router']);

thrum.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/home');

    $stateProvider
        
        .state('home', {
            url:'/home',
            templateUrl: '../views/home.html'
        })
        .state('about', {
            url: '/about',
            templateUrl: '../views/about.html'
        })
        .state('main', {
            url: '/main',
            templateUrl: '../views/main.html'
        })
        .state('main.trending', {
            url:'/trending',
            templateUrl:'../views/trending.html'
        })
        .state('main.wordtree', {
            url:'/wordtree',
            templateUrl:'../views/wordtree.html'
        })
        .state('main.search', {
            url:'/search',
            templateUrl:'../views/search.html'
        });
});