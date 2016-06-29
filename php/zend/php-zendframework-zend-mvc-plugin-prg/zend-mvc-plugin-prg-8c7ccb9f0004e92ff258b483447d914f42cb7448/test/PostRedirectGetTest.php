<?php
/**
 * @link      http://github.com/zendframework/zend-mvc-plugin-prg for the canonical source repository
 * @copyright Copyright (c) 2005-2016 Zend Technologies USA Inc. (http://www.zend.com)
 * @license   http://framework.zend.com/license/new-bsd New BSD License
 */

namespace ZendTest\Mvc\Plugin\Prg;

use PHPUnit_Framework_TestCase as TestCase;
use Zend\Http\Request;
use Zend\Http\Response;
use Zend\Mvc\MvcEvent;
use Zend\Mvc\ModuleRouteListener;
use Zend\Mvc\Plugin\Prg\PostRedirectGet;
use Zend\Router\Exception\RuntimeException;
use Zend\Router\Http\Literal as LiteralRoute;
use Zend\Router\Http\Segment as SegmentRoute;
use Zend\Router\RouteMatch;
use Zend\Router\SimpleRouteStack;
use Zend\Router\Http\TreeRouteStack;
use Zend\Stdlib\Parameters;

class PostRedirectGetTest extends TestCase
{
    public $controller;
    public $event;
    public $request;
    public $response;

    public function setUp()
    {
        $router = new TreeRouteStack;
        $router->addRoute('home', LiteralRoute::factory([
            'route'    => '/',
            'defaults' => [
                'controller' => TestAsset\SampleController::class,
            ]
        ]));

        $router->addRoute('sub', SegmentRoute::factory([
            'route' => '/foo/:param',
            'defaults' => [
                'param' => 1
            ]
        ]));

        $router->addRoute('ctl', SegmentRoute::factory([
            'route' => '/ctl/:controller',
            'defaults' => [
                '__NAMESPACE__' => 'ZendTest\Mvc\Plugin\Prg\TestAsset',
                'controller' => 'sample'
            ]
        ]));

        $this->controller = new TestAsset\SampleController();
        $this->request    = new Request();
        $this->event      = new MvcEvent();
        $this->routeMatch = new RouteMatch(['controller' => 'controller-sample', 'action' => 'postPage']);

        $this->event->setRequest($this->request);
        $this->event->setRouteMatch($this->routeMatch);
        $this->event->setRouter($router);

        $this->controller->setEvent($this->event);

        $this->plugin = new PostRedirectGet();
        $this->plugin->setController($this->controller);
    }

    public function testReturnsFalseOnInitialGet()
    {
        $this->controller->dispatch($this->request, $this->response);

        $plugin = $this->plugin;
        $this->assertFalse($plugin('home'));
    }

    public function testRedirectsToUrlOnPost()
    {
        $this->request->setMethod('POST');
        $this->request->setPost(new Parameters([
            'postval1' => 'value'
        ]));
        $this->controller->dispatch($this->request, $this->response);

        $plugin       = $this->plugin;
        $prgResultUrl = $plugin('/test/getPage', true);

        $this->assertInstanceOf('Zend\Http\Response', $prgResultUrl);
        $this->assertTrue($prgResultUrl->getHeaders()->has('Location'));
        $this->assertEquals('/test/getPage', $prgResultUrl->getHeaders()->get('Location')->getUri());
        $this->assertEquals(303, $prgResultUrl->getStatusCode());
    }

    public function testRedirectsToRouteOnPost()
    {
        $this->request->setMethod('POST');
        $this->request->setPost(new Parameters([
            'postval1' => 'value1'
        ]));
        $this->controller->dispatch($this->request, $this->response);

        $plugin         = $this->plugin;
        $prgResultRoute = $plugin('home');

        $this->assertInstanceOf('Zend\Http\Response', $prgResultRoute);
        $this->assertTrue($prgResultRoute->getHeaders()->has('Location'));
        $this->assertEquals('/', $prgResultRoute->getHeaders()->get('Location')->getUri());
        $this->assertEquals(303, $prgResultRoute->getStatusCode());
    }

    public function testReturnsPostOnRedirectGet()
    {
        $params = [
            'postval1' => 'value1'
        ];
        $this->request->setMethod('POST');
        $this->request->setPost(new Parameters($params));
        $this->controller->dispatch($this->request, $this->response);

        $plugin         = $this->plugin;
        $prgResultRoute = $plugin('home');

        $this->assertInstanceOf('Zend\Http\Response', $prgResultRoute);
        $this->assertTrue($prgResultRoute->getHeaders()->has('Location'));
        $this->assertEquals('/', $prgResultRoute->getHeaders()->get('Location')->getUri());
        $this->assertEquals(303, $prgResultRoute->getStatusCode());

        // Do GET
        $this->request = new Request();
        $this->controller->dispatch($this->request, $this->response);
        $prgResult = $plugin('home');

        $this->assertEquals($params, $prgResult);

        // Do GET again to make sure data is empty
        $this->request = new Request();
        $this->controller->dispatch($this->request, $this->response);
        $prgResult = $plugin('home');

        $this->assertFalse($prgResult);
    }

    public function testThrowsExceptionOnRouteWithoutRouter()
    {
        $controller = $this->controller;
        $controller = $controller->getEvent()->setRouter(new SimpleRouteStack);

        $this->request->setMethod('POST');
        $this->request->setPost(new Parameters([
            'postval1' => 'value'
        ]));
        $this->controller->dispatch($this->request, $this->response);

        $this->setExpectedException(RuntimeException::class);
        $plugin         = $this->plugin;
        $prgResultRoute = $plugin('some/route');
    }

    public function testNullRouteUsesMatchedRouteName()
    {
        $this->controller->getEvent()->getRouteMatch()->setMatchedRouteName('home');

        $this->request->setMethod('POST');
        $this->request->setPost(new Parameters([
            'postval1' => 'value1'
        ]));
        $this->controller->dispatch($this->request, $this->response);

        $plugin         = $this->plugin;
        $prgResultRoute = $plugin();

        $this->assertInstanceOf('Zend\Http\Response', $prgResultRoute);
        $this->assertTrue($prgResultRoute->getHeaders()->has('Location'));
        $this->assertEquals('/', $prgResultRoute->getHeaders()->get('Location')->getUri());
        $this->assertEquals(303, $prgResultRoute->getStatusCode());
    }

    public function testReuseMatchedParameters()
    {
        $this->controller->getEvent()->getRouteMatch()->setMatchedRouteName('sub');

        $this->request->setMethod('POST');
        $this->request->setPost(new Parameters([
            'postval1' => 'value1'
        ]));
        $this->controller->dispatch($this->request, $this->response);

        $plugin         = $this->plugin;
        $prgResultRoute = $plugin();

        $this->assertInstanceOf('Zend\Http\Response', $prgResultRoute);
        $this->assertTrue($prgResultRoute->getHeaders()->has('Location'));
        $this->assertEquals('/foo/1', $prgResultRoute->getHeaders()->get('Location')->getUri());
        $this->assertEquals(303, $prgResultRoute->getStatusCode());
    }

    public function testReuseMatchedParametersWithSegmentController()
    {
        $expects = '/ctl/sample';
        $this->request->setMethod('POST');
        $this->request->setUri($expects);
        $this->request->setPost(new Parameters([
            'postval1' => 'value1'
        ]));

        $routeMatch = $this->event->getRouter()->match($this->request);
        $this->event->setRouteMatch($routeMatch);

        $moduleRouteListener = new ModuleRouteListener;
        $moduleRouteListener->onRoute($this->event);

        $this->controller->dispatch($this->request, $this->response);

        $plugin         = $this->plugin;
        $prgResultRoute = $plugin();

        $this->assertInstanceOf('Zend\Http\Response', $prgResultRoute);
        $this->assertTrue($prgResultRoute->getHeaders()->has('Location'));
        $this->assertEquals(
            $expects,
            $prgResultRoute->getHeaders()->get('Location')->getUri(),
            'expects to redirect for the same url'
        );
        $this->assertEquals(303, $prgResultRoute->getStatusCode());
    }

    public function testKeepUrlQueryParameters()
    {
        $expects = '/ctl/sample';
        $this->request->setMethod('POST');
        $this->request->setUri($expects);
        $this->request->setQuery(new Parameters([
            'id' => '123',
        ]));

        $routeMatch = $this->event->getRouter()->match($this->request);
        $this->event->setRouteMatch($routeMatch);

        $moduleRouteListener = new ModuleRouteListener;
        $moduleRouteListener->onRoute($this->event);

        $this->controller->dispatch($this->request, $this->response);

        $plugin         = $this->plugin;
        $prgResultRoute = $plugin();

        $this->assertInstanceOf('Zend\Http\Response', $prgResultRoute);
        $this->assertTrue($prgResultRoute->getHeaders()->has('Location'));
        $this->assertEquals(
            $expects . '?id=123',
            $prgResultRoute->getHeaders()->get('Location')->getUri(),
            'expects to redirect for the same url'
        );
        $this->assertEquals(303, $prgResultRoute->getStatusCode());
    }
}
