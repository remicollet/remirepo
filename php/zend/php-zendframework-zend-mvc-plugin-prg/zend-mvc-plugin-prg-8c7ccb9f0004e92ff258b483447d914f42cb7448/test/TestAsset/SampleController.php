<?php
/**
 * @link      http://github.com/zendframework/zend-mvc-plugin-prg for the canonical source repository
 * @copyright Copyright (c) 2005-2016 Zend Technologies USA Inc. (http://www.zend.com)
 * @license   http://framework.zend.com/license/new-bsd New BSD License
 */

namespace ZendTest\Mvc\Plugin\Prg\TestAsset;

use Zend\Mvc\Controller\AbstractActionController;

class SampleController extends AbstractActionController
{
    /**
     * Override notFoundAction() to work as a no-op.
     */
    public function notFoundAction()
    {
    }
}
