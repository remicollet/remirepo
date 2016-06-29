<?php
/**
 * @link      http://github.com/zendframework/zend-mvc-plugin-prg for the canonical source repository
 * @copyright Copyright (c) 2005-2016 Zend Technologies USA Inc. (http://www.zend.com)
 * @license   http://framework.zend.com/license/new-bsd New BSD License
 */

namespace Zend\Mvc\Plugin\Prg;

use Zend\ServiceManager\Factory\InvokableFactory;

class Module
{
    /**
     * Provide application configuration.
     *
     * Adds aliases and factories for the PostRedirectGet plugin.
     *
     * @return array
     */
    public function getConfig()
    {
        return [
            'controller_plugins' => [
                'aliases' => [
                    'prg'             => PostRedirectGet::class,
                    'PostRedirectGet' => PostRedirectGet::class,
                    'postRedirectGet' => PostRedirectGet::class,
                    'postredirectget' => PostRedirectGet::class,
                    'Zend\Mvc\Controller\Plugin\PostRedirectGet' => PostRedirectGet::class,
                ],
                'factories' => [
                    PostRedirectGet::class => InvokableFactory::class,
                ],
            ],
        ];
    }
}
