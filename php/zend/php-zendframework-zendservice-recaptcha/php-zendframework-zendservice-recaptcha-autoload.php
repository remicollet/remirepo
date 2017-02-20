<?php
/*
Simple autoloader for Zend Framework + ZendService components
Inspired from https://github.com/zendframework/ZendSkeletonApplication

Set autoregister_zf     for Zend Framework
Set fallback_autoloader for dependencies which are PSR-0 compliant
*/
require_once '/usr/share/php/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'fallback_autoloader' => true,
        'autoregister_zf' => true,
        'namespaces' => array(
           'ZendService' => dirname(__DIR__)
))));
