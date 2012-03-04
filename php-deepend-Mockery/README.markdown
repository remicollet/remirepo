


<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# githubog: http://ogp.me/ns/fb/githubog#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>mockery/README.markdown at master · padraic/mockery · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />

    
    

    <meta content="authenticity_token" name="csrf-param" />
<meta content="mZDiC48jghul0hyB6ymLLJii5HG0uyC107YAvlojuPk=" name="csrf-token" />

    <link href="https://a248.e.akamai.net/assets.github.com/stylesheets/bundles/github-c4b3a1e3484da7dab93ea4f6caca07a0168ffa77.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="https://a248.e.akamai.net/assets.github.com/stylesheets/bundles/github2-34d96ae148c427d3106177152ac475d7df36c780.css" media="screen" rel="stylesheet" type="text/css" />
    

    <script src="https://a248.e.akamai.net/assets.github.com/javascripts/bundles/jquery-5b140862bd914d3619171dece9be92269c2b1fe1.js" type="text/javascript"></script>
    <script src="https://a248.e.akamai.net/assets.github.com/javascripts/bundles/github-1191d9500b9368ede4221610a2d9c453c0cb35f8.js" type="text/javascript"></script>
    

      <link rel='permalink' href='/padraic/mockery/blob/2c5e3244b72d268d8c70935fcceb39b3d84d57db/README.markdown'>
    <meta property="og:title" content="mockery"/>
    <meta property="og:type" content="githubog:gitrepository"/>
    <meta property="og:url" content="https://github.com/padraic/mockery"/>
    <meta property="og:image" content="https://a248.e.akamai.net/assets.github.com/images/gravatars/gravatar-140.png?1329275856"/>
    <meta property="og:site_name" content="GitHub"/>
    <meta property="og:description" content="mockery - Mockery is a simple yet flexible PHP mock object framework for use in unit testing with PHPUnit, PHPSpec or any other testing framework. Its core goal is to offer a test double framework with a succint API capable of clearly defining all possible object operations and interactions using a human readable Domain Specific Language (DSL). Designed as a drop in alternative to PHPUnit's phpunit-mock-objects library, Mockery is easy to integrate with PHPUnit and can operate alongside phpunit-mock-objects without the World ending. "/>

    <meta name="description" content="mockery - Mockery is a simple yet flexible PHP mock object framework for use in unit testing with PHPUnit, PHPSpec or any other testing framework. Its core goal is to offer a test double framework with a succint API capable of clearly defining all possible object operations and interactions using a human readable Domain Specific Language (DSL). Designed as a drop in alternative to PHPUnit's phpunit-mock-objects library, Mockery is easy to integrate with PHPUnit and can operate alongside phpunit-mock-objects without the World ending. " />
  <link href="https://github.com/padraic/mockery/commits/master.atom" rel="alternate" title="Recent Commits to mockery:master" type="application/atom+xml" />

  </head>


  <body class="logged_out page-blob  vis-public env-production " data-blob-contribs-enabled="yes">
    
    
    

      <div id="header" class="true clearfix">
        <div class="container clearfix">
          <a class="site-logo" href="https://github.com">
            <!--[if IE]>
            <img alt="GitHub" class="github-logo" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7.png?1323882716" />
            <img alt="GitHub" class="github-logo-hover" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7-hover.png?1324325358" />
            <![endif]-->
            <img alt="GitHub" class="github-logo-4x" height="30" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7@4x.png?1323882716" />
            <img alt="GitHub" class="github-logo-4x-hover" height="30" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7@4x-hover.png?1324325358" />
          </a>

                  <!--
      make sure to use fully qualified URLs here since this nav
      is used on error pages on other domains
    -->
    <ul class="top-nav logged_out">
        <li class="pricing"><a href="https://github.com/plans">Signup and Pricing</a></li>
        <li class="explore"><a href="https://github.com/explore">Explore GitHub</a></li>
      <li class="features"><a href="https://github.com/features">Features</a></li>
        <li class="blog"><a href="https://github.com/blog">Blog</a></li>
      <li class="login"><a href="https://github.com/login?return_to=%2Fpadraic%2Fmockery%2Fblob%2Fmaster%2FREADME.markdown">Login</a></li>
    </ul>



          
        </div>
      </div>

      

            <div class="site">
      <div class="container">
        <div class="pagehead repohead instapaper_ignore readability-menu">
        <div class="title-actions-bar">
          <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
<a href="/padraic" itemprop="url">            <span itemprop="title">padraic</span>
            </a> /
            <strong><a href="/padraic/mockery" class="js-current-repository">mockery</a></strong>
          </h1>
          



              <ul class="pagehead-actions">


          <li><a href="/login?return_to=%2Fpadraic%2Fmockery" class="minibutton btn-watch watch-button entice tooltipped leftwards" rel="nofollow" title="You must be logged in to use this feature"><span><span class="icon"></span>Watch</span></a></li>
          <li><a href="/login?return_to=%2Fpadraic%2Fmockery" class="minibutton btn-fork fork-button entice tooltipped leftwards" rel="nofollow" title="You must be logged in to use this feature"><span><span class="icon"></span>Fork</span></a></li>


      <li class="repostats">
        <ul class="repo-stats">
          <li class="watchers ">
            <a href="/padraic/mockery/watchers" title="Watchers" class="tooltipped downwards">
              301
            </a>
          </li>
          <li class="forks">
            <a href="/padraic/mockery/network" title="Forks" class="tooltipped downwards">
              35
            </a>
          </li>
        </ul>
      </li>
    </ul>

        </div>

          

  <ul class="tabs">
    <li><a href="/padraic/mockery" class="selected" highlight="repo_sourcerepo_downloadsrepo_commitsrepo_tagsrepo_branches">Code</a></li>
    <li><a href="/padraic/mockery/network" highlight="repo_networkrepo_fork_queue">Network</a>
    <li><a href="/padraic/mockery/pulls" highlight="repo_pulls">Pull Requests <span class='counter'>3</span></a></li>

      <li><a href="/padraic/mockery/issues" highlight="repo_issues">Issues <span class='counter'>8</span></a></li>


    <li><a href="/padraic/mockery/graphs" highlight="repo_graphsrepo_contributors">Stats &amp; Graphs</a></li>

  </ul>

  
<div class="frame frame-center tree-finder" style="display:none"
      data-tree-list-url="/padraic/mockery/tree-list/2c5e3244b72d268d8c70935fcceb39b3d84d57db"
      data-blob-url-prefix="/padraic/mockery/blob/2c5e3244b72d268d8c70935fcceb39b3d84d57db"
    >

  <div class="breadcrumb">
    <span class="bold"><a href="/padraic/mockery">mockery</a></span> /
    <input class="tree-finder-input js-navigation-enable" type="text" name="query" autocomplete="off" spellcheck="false">
  </div>

    <div class="octotip">
      <p>
        <a href="/padraic/mockery/dismiss-tree-finder-help" class="dismiss js-dismiss-tree-list-help" title="Hide this notice forever" rel="nofollow">Dismiss</a>
        <span class="bold">Octotip:</span> You've activated the <em>file finder</em>
        by pressing <span class="kbd">t</span> Start typing to filter the
        file list. Use <span class="kbd badmono">↑</span> and
        <span class="kbd badmono">↓</span> to navigate,
        <span class="kbd">enter</span> to view files.
      </p>
    </div>

  <table class="tree-browser" cellpadding="0" cellspacing="0">
    <tr class="js-header"><th>&nbsp;</th><th>name</th></tr>
    <tr class="js-no-results no-results" style="display: none">
      <th colspan="2">No matching files</th>
    </tr>
    <tbody class="js-results-list js-navigation-container">
    </tbody>
  </table>
</div>

<div id="jump-to-line" style="display:none">
  <h2>Jump to Line</h2>
  <form>
    <input class="textfield" type="text">
    <div class="full-button">
      <button type="submit" class="classy">
        <span>Go</span>
      </button>
    </div>
  </form>
</div>


<div class="subnav-bar">

  <ul class="actions subnav">
    <li><a href="/padraic/mockery/tags" class="" highlight="repo_tags">Tags <span class="counter">6</span></a></li>
    <li><a href="/padraic/mockery/downloads" class="blank downloads-blank" highlight="repo_downloads">Downloads <span class="counter">0</span></a></li>
    
  </ul>

  <ul class="scope">
    <li class="switcher">

      <div class="context-menu-container js-menu-container">
        <a href="#"
           class="minibutton bigger switcher js-menu-target js-commitish-button btn-branch repo-tree"
           data-master-branch="master"
           data-ref="master">
          <span><span class="icon"></span><i>branch:</i> master</span>
        </a>

        <div class="context-pane commitish-context js-menu-content">
          <a href="javascript:;" class="close js-menu-close"></a>
          <div class="context-title">Switch Branches/Tags</div>
          <div class="context-body pane-selector commitish-selector js-filterable-commitishes">
            <div class="filterbar">
              <div class="placeholder-field js-placeholder-field">
                <label class="placeholder" for="context-commitish-filter-field" data-placeholder-mode="sticky">Filter branches/tags</label>
                <input type="text" id="context-commitish-filter-field" class="commitish-filter" />
              </div>

              <ul class="tabs">
                <li><a href="#" data-filter="branches" class="selected">Branches</a></li>
                <li><a href="#" data-filter="tags">Tags</a></li>
              </ul>
            </div>

              <div class="commitish-item branch-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/0.6/README.markdown" data-name="0.6" rel="nofollow">0.6</a>
                </h4>
              </div>
              <div class="commitish-item branch-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/master/README.markdown" data-name="master" rel="nofollow">master</a>
                </h4>
              </div>
              <div class="commitish-item branch-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/prototype/README.markdown" data-name="prototype" rel="nofollow">prototype</a>
                </h4>
              </div>
              <div class="commitish-item branch-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/testspy/README.markdown" data-name="testspy" rel="nofollow">testspy</a>
                </h4>
              </div>

              <div class="commitish-item tag-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/0.7.2/README.markdown" data-name="0.7.2" rel="nofollow">0.7.2</a>
                </h4>
              </div>
              <div class="commitish-item tag-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/0.7.0/README.markdown" data-name="0.7.0" rel="nofollow">0.7.0</a>
                </h4>
              </div>
              <div class="commitish-item tag-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/0.6.3/README.markdown" data-name="0.6.3" rel="nofollow">0.6.3</a>
                </h4>
              </div>
              <div class="commitish-item tag-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/0.6.2/README.markdown" data-name="0.6.2" rel="nofollow">0.6.2</a>
                </h4>
              </div>
              <div class="commitish-item tag-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/0.6.1/README.markdown" data-name="0.6.1" rel="nofollow">0.6.1</a>
                </h4>
              </div>
              <div class="commitish-item tag-commitish selector-item">
                <h4>
                    <a href="/padraic/mockery/blob/0.6.0/README.markdown" data-name="0.6.0" rel="nofollow">0.6.0</a>
                </h4>
              </div>

            <div class="no-results" style="display:none">Nothing to show</div>
          </div>
        </div><!-- /.commitish-context-context -->
      </div>

    </li>
  </ul>

  <ul class="subnav with-scope">

    <li><a href="/padraic/mockery" class="selected" highlight="repo_source">Files</a></li>
    <li><a href="/padraic/mockery/commits/master" highlight="repo_commits">Commits</a></li>
    <li><a href="/padraic/mockery/branches" class="" highlight="repo_branches" rel="nofollow">Branches <span class="counter">4</span></a></li>
  </ul>

</div>

  
  
  


          

        </div><!-- /.repohead -->

        





<!-- block_view_fragment_key: views4/v8/blob:v17:c1d0dd948a0321733305a84294a70666 -->
  <div id="slider">

    <div class="breadcrumb" data-path="README.markdown/">
      <b itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/padraic/mockery/tree/2c5e3244b72d268d8c70935fcceb39b3d84d57db" class="js-rewrite-sha" itemprop="url"><span itemprop="title">mockery</span></a></b> / <strong class="final-path">README.markdown</strong> <span class="js-clippy clippy-button " data-clipboard-text="README.markdown" data-copied-hint="copied!" data-copy-hint="copy to clipboard"></span>
    </div>


      <div class="commit file-history-tease" data-path="README.markdown/">
        <img class="main-avatar" height="24" src="https://secure.gravatar.com/avatar/94a0e0f46ab92fc828436bea73c53583?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png" width="24" />
        <span class="author"><a href="/padraic">padraic</a></span>
        <time class="js-relative-date" datetime="2012-01-28T11:40:18-08:00" title="2012-01-28 11:40:18">January 28, 2012</time>
        <div class="commit-title">
            <a href="/padraic/mockery/commit/2c5e3244b72d268d8c70935fcceb39b3d84d57db" class="message">Updated README to show Travis CI build status</a>
        </div>

        <div class="participation">
          <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>2</strong> contributors</a></p>
              <a class="avatar tooltipped downwards" title="padraic" href="/padraic/mockery/commits/master/README.markdown?author=padraic"><img height="20" src="https://secure.gravatar.com/avatar/94a0e0f46ab92fc828436bea73c53583?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png" width="20" /><span class="overlay size-20"></span></a>
    <a class="avatar tooltipped downwards" title="rdohms" href="/padraic/mockery/commits/master/README.markdown?author=rdohms"><img height="20" src="https://secure.gravatar.com/avatar/d9545121873fb2829737d5c385f62214?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png" width="20" /><span class="overlay size-20"></span></a>


        </div>
        <div id="blob_contributors_box" style="display:none">
          <h2>Users on GitHub who have contributed to this file</h2>
          <ul class="facebox-user-list">
            <li>
              <img height="24" src="https://secure.gravatar.com/avatar/94a0e0f46ab92fc828436bea73c53583?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png" width="24" />
              <a href="/padraic">padraic</a>
            </li>
            <li>
              <img height="24" src="https://secure.gravatar.com/avatar/d9545121873fb2829737d5c385f62214?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png" width="24" />
              <a href="/rdohms">rdohms</a>
            </li>
          </ul>
        </div>
      </div>

    <div class="frames">
      <div class="frame frame-center" data-path="README.markdown/" data-permalink-url="/padraic/mockery/blob/2c5e3244b72d268d8c70935fcceb39b3d84d57db/README.markdown" data-title="mockery/README.markdown at master · padraic/mockery · GitHub" data-type="blob">

        <div id="files" class="bubble">
          <div class="file">
            <div class="meta">
              <div class="info">
                <span class="icon"><img alt="Txt" height="16" src="https://a248.e.akamai.net/assets.github.com/images/icons/txt.png?1310086001" width="16" /></span>
                <span class="mode" title="File Mode">100644</span>
                  <span>1113 lines (816 sloc)</span>
                <span>45.775 kb</span>
              </div>
              <ul class="button-group actions">
                  <li>
                    <a class="grouped-button file-edit-link minibutton bigger lighter js-rewrite-sha" href="/padraic/mockery/edit/2c5e3244b72d268d8c70935fcceb39b3d84d57db/README.markdown" data-method="post" rel="nofollow"><span>Edit this file</span></a>
                  </li>

                <li>
                  <a href="/padraic/mockery/raw/master/README.markdown" class="minibutton btn-raw grouped-button bigger lighter" id="raw-url"><span><span class="icon"></span>Raw</span></a>
                </li>
                  <li>
                    <a href="/padraic/mockery/blame/master/README.markdown" class="minibutton btn-blame grouped-button bigger lighter"><span><span class="icon"></span>Blame</span></a>
                  </li>
                <li>
                  <a href="/padraic/mockery/commits/master/README.markdown" class="minibutton btn-history grouped-button bigger lighter" rel="nofollow"><span><span class="icon"></span>History</span></a>
                </li>
              </ul>
            </div>
            
  <div id="readme" class="blob instapaper_body">
    <article class="markdown-body"><h1>Mockery</h1>

<p>Mockery is a simple yet flexible PHP mock object framework for use in unit testing
with PHPUnit, PHPSpec or any other testing framework. Its core goal is to offer a
test double framework with a succint API capable of clearly defining all possible
object operations and interactions using a human readable Domain Specific Language
(DSL). Designed as a drop in alternative to PHPUnit's phpunit-mock-objects library,
Mockery is easy to integrate with PHPUnit and can operate alongside
phpunit-mock-objects without the World ending.</p>

<p>Mockery is released under a New BSD License.</p>

<p>The current stable version is Mockery 0.7.2.
The build status of the current master branch is tracked by Travis CI:
<a href="http://travis-ci.org/padraic/mockery"><img src="https://secure.travis-ci.org/padraic/mockery.png" alt="Build Status"></a></p>

<h2>Mock Objects</h2>

<p>In unit tests, mock objects simulate the behaviour of real objects. They are
commonly utilised to offer test isolation, to stand in for objects which do not
yet exist, or to allow for the exploratory design of class APIs without
requiring actual implementation up front.</p>

<p>The benefits of a mock object framework are to allow for the flexible generation
of such mock objects (and stubs). They allow the setting of expected method calls
and return values using a flexible API which is capable of capturing every
possible real object behaviour in way that is stated as close as possible to a
natural language description.</p>

<h2>Prerequisites</h2>

<p>Mockery requires PHP 5.3.2 or greater. In addition, it is strongly recommended to install
the Hamcrest library (see below for instructions).</p>

<h2>Installation</h2>

<p>Mockery may be installed using Composer, PEAR or by cloning it from its Github repository. These
three options are outlined below.</p>

<p><strong>Composer</strong></p>

<p>You can read more about Composer and its main repository at
<a href="http://packagist.org" title="Packagist"></a><a href="http://packagist.org">http://packagist.org</a>. To install
Mockery using Composer, first install Composer for your project using the instructions on the
Packagist home page. You can then define your dependency on Mockery using the suggested parameters below.</p>

<pre><code>{
    "require": {
        "mockery/mockery": "&gt;=0.7.2"
    }
}
</code></pre>

<p><strong>PEAR</strong></p>

<p>Mockery is hosted on the <a href="http://pear.survivethedeepend.com">survivethedeepend.com</a> PEAR channel and
can be installed using the following commands:</p>

<pre><code>sudo pear channel-discover pear.survivethedeepend.com
sudo pear channel-discover hamcrest.googlecode.com/svn/pear
sudo pear install --alldeps deepend/Mockery
</code></pre>

<p><strong>Git / Github</strong></p>

<p>The git repository hosts the development version in its master branch. You may
install this development version using:</p>

<pre><code>git clone git://github.com/padraic/mockery.git
cd mockery
sudo pear channel-discover hamcrest.googlecode.com/svn/pear
sudo pear install --alldeps package.xml
</code></pre>

<p>The above processes will install both Mockery and Hamcrest.
While omitting Hamcrest will not break Mockery, Hamcrest is highly recommended
as it adds a wider variety of functionality for argument matching that Mockery
is capable of.</p>

<h2>Simple Example</h2>

<p>Imagine we have a Temperature class which samples the temperature of a locale
before reporting an average temperature. The data could come from a web service
or any other data source, but we do not have such a class at present. We can,
however, assume some basic interactions with such a class based on its interaction
with the Temperature class.</p>

<pre><code>class Temperature
{

    public function __construct($service)
    {
        $this-&gt;_service = $service;
    }

    public function average()
    {
        $total = 0;
        for ($i=0;$i&lt;3;$i++) {
            $total += $this-&gt;_service-&gt;readTemp();
        }
        return $total/3;
    }

}
</code></pre>

<p>Even without an actual service class, we can see how we expect it to operate.
When writing a test for the Temperature class, we can now substitute a mock
object for the real service which allows us to test the behaviour of the
Temperature class without actually needing a concrete service instance.</p>

<p>Note: PHPUnit integration (see below) can remove the need for a teardown() method.</p>

<pre><code>use \Mockery as m;

class TemperatureTest extends PHPUnit_Framework_TestCase
{

    public function teardown()
    {
        m::close();
    }

    public function testGetsAverageTemperatureFromThreeServiceReadings()
    {
        $service = m::mock('service');
        $service-&gt;shouldReceive('readTemp')-&gt;times(3)-&gt;andReturn(10, 12, 14);
        $temperature = new Temperature($service);
        $this-&gt;assertEquals(12, $temperature-&gt;average());
    }

}
</code></pre>

<p>We'll cover the API in greater detail below.</p>

<h2>PHPUnit Integration</h2>

<p>Mockery was designed as a simple to use standalone mock object framework, so
its need for integration with any testing framework is entirely optional.
To integrate Mockery, you just need to define a teardown() method for your
tests containing the following (you may use a shorter \Mockery namespace alias):</p>

<pre><code>public function teardown() {
    \Mockery::close();
}
</code></pre>

<p>This static call cleans up the Mockery container used by the current test, and
run any verification tasks needed for your expectations.</p>

<p>For some added brevity when it comes to using Mockery, you can also explicitly
use the Mockery namespace with a shorter alias. For example:</p>

<pre><code>use \Mockery as m;

class SimpleTest extends PHPUnit_Framework_TestCase
{
    public function testSimpleMock() {
        $mock = m::mock('simple mock');
        $mock-&gt;shouldReceive('foo')-&gt;with(5, m::any())-&gt;once()-&gt;andReturn(10);
        $this-&gt;assertEquals(10, $mock-&gt;foo(5));
    }

    public function teardown() {
        m::close();
    }
}
</code></pre>

<p>Mockery ships with an autoloader so you don't need to litter your tests with
require_once() calls. To use it, ensure Mockery is on your include_path and add
the following to your test suite's Bootstrap.php or TestHelper.php file:</p>

<pre><code>require_once 'Mockery/Loader.php';
require_once 'Hamcrest/Hamcrest.php';
$loader = new \Mockery\Loader;
$loader-&gt;register();
</code></pre>

<p>(Note: Prior to Hamcrest 1.0.0, the Hamcrest.php file name had a small "h", i.e. hamcrest.php. If upgrading Hamcrest to 1.0.0 remember to check the file name is updated for all your projects.)</p>

<p>To integrate Mockery into PHPUnit and avoid having to call the close method and
have Mockery remove itself from code coverage reports, use this in you suite:</p>

<pre><code>//Create Suite
$suite = new PHPUnit_Framework_TestSuite();

//Create a result listener or add it
$result = new PHPUnit_Framework_TestResult();
    $result-&gt;addListener(new \Mockery\Adapter\Phpunit\TestListener());

// Run the tests.
$suite-&gt;run($result);
</code></pre>

<p>If you are using PHPUnit's XML configuration approach, you can include the following to load the TestListener:</p>

<pre><code>&lt;listeners&gt;
    &lt;listener class="\Mockery\Adapter\Phpunit\TestListener" file="Mockery/Adapter/Phpunit/TestListener.php"&gt;&lt;/listener&gt;
&lt;/listeners&gt;
</code></pre>

<h2>Quick Reference</h2>

<p>Mockery implements a shorthand API when creating a mock. Here's a sampling
of the possible startup methods.</p>

<pre><code>$mock = \Mockery::mock('foo');
</code></pre>

<p>Creates a mock object named foo. In this case, foo is a name (not necessarily
a class name) used as a simple identifier when raising exceptions. This creates
a mock object of type \Mockery\Mock and is the loosest form of mock possible.</p>

<pre><code>$mock = \Mockery::mock(array('foo'=&gt;1,'bar'=&gt;2));
</code></pre>

<p>Creates an mock object named unknown since we passed no name. However we did
pass an expectation array, a quick method of setting up methods to expect with
their return values.</p>

<pre><code>$mock = \Mockery::mock('foo', array('foo'=&gt;1,'bar'=&gt;2));
</code></pre>

<p>Similar to the previous examples and all examples going forward, expectation arrays
can be passed for all mock objects as the second parameter to mock().</p>

<pre><code>$mock = \Mockery::mock('foo', function($mock) {
    $mock-&gt;shouldReceive(method_name);
});
</code></pre>

<p>In addition to expectation arrays, you can also pass in a closure which contains
reusable expectations. This can be passed as the second parameter, or as the third
parameter if partnered with an expectation array. This is one method for creating
reusable mock expectations.</p>

<pre><code>$mock = \Mockery::mock('stdClass');
</code></pre>

<p>Creates a mock identical to a named mock, except the name is an actual class
name. Creates a simple mock as previous examples show, except the mock
object will inherit the class type (via inheritance), i.e. it will pass type hints
or instanceof evaluations for stdClass. Useful where a mock object must be of a specific
type.</p>

<pre><code>$mock = \Mockery::mock('FooInterface');
</code></pre>

<p>You can create mock objects based on any concrete class, abstract class or
even an interface. Again, the primary purpose is to ensure the mock object
inherits a specific type for type hinting. There is an exception in that classes
marked final, or with methods marked final, cannot be mocked fully. In these cases
a partial mock (explained below) must be utilised.</p>

<pre><code>$mock = \Mockery::mock('alias:MyNamespace\MyClass');
</code></pre>

<p>Prefixing the valid name of a class (which is NOT currently loaded) with "alias:"
will generate an "alias mock". Alias mocks create a class alias with the given
classname to stdClass and are generally used to enable the mocking of public
static methods. Expectations set on the new mock object which refer to static
methods will be used by all static calls to this class.</p>

<pre><code>$mock = \Mockery::mock('overload:MyNamespace\MyClass');
</code></pre>

<p>Prefixing the valid name of a class (which is NOT currently loaded) with "overload:" will
generate an alias mock (as with "alias:") except that created new instances of that
class will import any expectations set on the origin mock ($mock). The origin
mock is never verified since it's used an expectation store for new instances. For this
purpose I used the term "instance mock" to differentiate it from the simpler "alias mock".</p>

<p>Note: Using alias/instance mocks across more than one test will generate a fatal error since
you can't have two classes of the same name. To avoid this, run each test of this
kind in a separate PHP process (which is supported out of the box by both
PHPUnit and PHPT).</p>

<pre><code>$mock = \Mockery::mock('stdClass, MyInterface1, MyInterface2');
</code></pre>

<p>The first argument can also accept a list of interfaces that the mock object must
implement, optionally including no more than one existing class to be based on. The
class name doesn't need to be the first member of the list but it's a friendly
convention to use for readability. All subsequent arguments remain unchanged from
previous examples.</p>

<pre><code>$mock = \Mockery::mock('MyNamespace\MyClass[foo,bar]');
</code></pre>

<p>The syntax above tells Mockery to partially mock the MyNamespace\MyClass class,
by mocking the foo() and bar() methods only. Any other method will be not be
overridden by Mockery. This form of "partial mock" can be applied to any class
or abstract class (e.g. mocking abstract methods where a concrete implementation
does not exist yet).</p>

<pre><code>$mock = \Mockery::mock(new Foo);
</code></pre>

<p>Passing any real object into Mockery will create a partial mock. Partials assume
you can already create a concrete object, so all we need to do is selectively
override a subset of existing methods (or add non-existing methods!) for
our expectations. Partial mocks are essential for any class which is marked final
or contains public methods marked final.</p>

<p>A little revision: All mock methods accept the class, object or alias name to be
mocked as the first parameter. The second parameter can be an expectation array
of methods and their return values, or an expectation closure (which can be the
third param if used in conjunction with an expectation array).</p>

<pre><code>\Mockery::self()
</code></pre>

<p>At times, you will discover that expectations on a mock include methods which need to return the same mock object (e.g. a common case when designing a Domain Specific Language (DSL) such as the one Mockery itself uses!). To facilitate this, calling \Mockery::self() will always return the last Mock Object created by calling \Mockery::mock(). For example:</p>

<pre><code>$mock = \Mockery::mock('BazIterator')
    -&gt;shouldReceive('next')
    -&gt;andReturn(\Mockery::self());
</code></pre>

<p>The above class being mocked, as the next() method suggests, is an iterator. In many cases, you can replace all the iterated elements (since they are the same type many times) with just the one mock object which is programmed to act as discrete iterated elements.</p>

<h2>Expectation Declarations</h2>

<p>Once you have created a mock object, you'll often want to start defining how
exactly it should behave (and how it should be called). This is where the
Mockery expectation declarations take over.</p>

<pre><code>shouldReceive(method_name)
</code></pre>

<p>Declares that the mock expects a call to the given method name. This is the
starting expectation upon which all other expectations and constraints are
appended.</p>

<pre><code>shouldReceive(method1, method2, ...)
</code></pre>

<p>Declares a number of expected method calls, all of which will adopt any chained
expectations or constraints.</p>

<pre><code>shouldReceive(array('method1'=&gt;1, 'method2'=&gt;2, ...))
</code></pre>

<p>Declares a number of expected calls but also their return values. All will
adopt any additional chained expectations or constraints.</p>

<pre><code>shouldReceive(closure)
</code></pre>

<p>Creates a mock object (only from a partial mock) which is used to create a mock
object recorder. The recorder is a simple proxy to the original object passed
in for mocking. This is passed to the closure, which may run it through a set of
operations which are recorded as expectations on the partial mock. A simple
use case is automatically recording expectations based on an existing usage
(e.g. during refactoring). See examples in a later section.</p>

<pre><code>with(arg1, arg2, ...)
</code></pre>

<p>Adds a constraint that this expectation only applies to method calls which
match the expected argument list. You can add a lot more flexibility to argument
matching using the built in matcher classes (see later). For example,
\Mockery::any() matches any argument passed to that position in the with()
parameter list. Mockery also allows Hamcrest library matchers - for example, the
Hamcrest function anything() is equivalent to \Mockery:any().</p>

<p>It's important to note that this means all expectations attached only apply
to the given method when it is called with these exact arguments. This allows for
setting up differing expectations based on the arguments provided to expected calls.</p>

<pre><code>withAnyArgs()
</code></pre>

<p>Declares that this expectation matches a method call regardless of what arguments
are passed. This is set by default unless otherwise specified.</p>

<pre><code>withNoArgs()
</code></pre>

<p>Declares this expectation matches method calls with zero arguments.</p>

<pre><code>andReturn(value)
</code></pre>

<p>Sets a value to be returned from the expected method call.</p>

<pre><code>andReturn(value1, value2, ...)
</code></pre>

<p>Sets up a sequence of return values or closures. For example, the first call will return
value1 and the second value2. Not that all subsequent calls to a mocked method
will always return the final value (or the only value) given to this declaration.</p>

<pre><code>andReturnUsing(closure, ...)
</code></pre>

<p>Sets a closure (anonymous function) to be called with the arguments passed to
the method. The return value from the closure is then returned. Useful for some
dynamic processing of arguments into related concrete results. Closures can
queued by passing them as extra parameters as for andReturn(). Note that you
cannot currently mix andReturnUsing() with andReturn().</p>

<pre><code>andThrow(Exception)
</code></pre>

<p>Declares that this method will throw the given Exception object when called.</p>

<pre><code>andThrow(exception_name, message)
</code></pre>

<p>Rather than an object, you can pass in the Exception class and message to
use when throwing an Exception from the mocked method.</p>

<pre><code>andSet(name, value1) / set(name, value1)
</code></pre>

<p>Used with an expectation so that when a matching method is called, one
can also cause a mock object's public property to be set to a specified value.</p>

<pre><code>zeroOrMoreTimes()
</code></pre>

<p>Declares that the expected method may be called zero or more times. This is
the default for all methods unless otherwise set.</p>

<pre><code>once()
</code></pre>

<p>Declares that the expected method may only be called once. Like all other
call count constraints, it will throw a \Mockery\CountValidator\Exception
if breached and can be modified by the atLeast() and atMost() constraints.</p>

<pre><code>twice()
</code></pre>

<p>Declares that the expected method may only be called twice.</p>

<pre><code>times(n)
</code></pre>

<p>Declares that the expected method may only be called n times.</p>

<pre><code>never()
</code></pre>

<p>Declares that the expected method may never be called. Ever!</p>

<pre><code>atLeast()
</code></pre>

<p>Adds a minimum modifier to the next call count expectation. Thus
atLeast()-&gt;times(3) means the call must be called at least three times (given
matching method args) but never less than three times.</p>

<pre><code>atMost()
</code></pre>

<p>Adds a maximum modifier to the next call count expectation. Thus
atMost()-&gt;times(3) means the call must be called no more than three times. This
also means no calls are acceptable.</p>

<pre><code>between(min, max)
</code></pre>

<p>Sets an expected range of call counts. This is actually identical to using
atLeast()-&gt;times(min)-&gt;atMost()-&gt;times(max) but is provided as a shorthand.
It may be followed by a times() call with no parameter to preserve the
APIs natural language readability.</p>

<pre><code>ordered()
</code></pre>

<p>Declares that this method is expected to be called in a specific order in
relation to similarly marked methods. The order is dictated by the order in
which this modifier is actually used when setting up mocks.</p>

<pre><code>ordered(group)
</code></pre>

<p>Declares the method as belonging to an order group (which can be named or
numbered). Methods within a group can be called in any order, but the ordered
calls from outside the group are ordered in relation to the group, i.e. you can
set up so that method1 is called before group1 which is in turn called before
method 2.</p>

<pre><code>globally()
</code></pre>

<p>When called prior to ordered() or ordered(group), it declares this ordering to
apply across all mock objects (not just the current mock). This allows for dictating
order expectations across multiple mocks.</p>

<pre><code>byDefault()
</code></pre>

<p>Marks an expectation as a default. Default expectations are applied unless
a non-default expectation is created. These later expectations immediately
replace the previously defined default. This is useful so you can setup default
mocks in your unit test setup() and later tweak them in specific tests as
needed.</p>

<pre><code>mock()
</code></pre>

<p>Returns the current mock object from an expectation chain. Useful where
you prefer to keep mock setups as a single statement, e.g.</p>

<pre><code>$mock = \Mockery::mock('foo')-&gt;shouldReceive('foo')-&gt;andReturn(1)-&gt;mock();
</code></pre>

<h2>Argument Validation</h2>

<p>The arguments passed to the with() declaration when setting up an expectation
determine the criteria for matching method calls to expectations. Thus, you
can setup up many expectations for a single method, each differentiated by
the expected arguments. Such argument matching is done on a "best fit" basis.
This ensures explicit matches take precedence over generalised matches.</p>

<p>An explicit match is merely where the expected argument and the actual argument
are easily equated (i.e. using === or ==). More generalised matches are possible
using regular expressions, class hinting and the available generic matchers. The
purpose of generalised matchers is to allow arguments be defined in non-explicit
terms, e.g. Mockery::any() passed to with() will match ANY argument in that
position.</p>

<p>Mockery's generic matchers do not cover all possibilities but offers optional
support for the Hamcrest library of matchers. Hamcrest is a PHP port of the
similarly named Java library (which has been ported also to Python, Erlang, etc).
I strongly recommend using Hamcrest since Mockery simply does not need to duplicate
Hamcrest's already impressive utility which itself promotes a natural English DSL.</p>

<p>The example below show Mockery matchers and their Hamcrest equivalent. Hamcrest uses
functions (no namespacing).</p>

<p>Here's a sample of the possibilities.</p>

<pre><code>with(1)
</code></pre>

<p>Matches the integer 1. This passes the === test (identical). It does facilitate
a less strict == check (equals) where the string '1' would also match the
argument.</p>

<pre><code>with(\Mockery::any()) OR with(anything())
</code></pre>

<p>Matches any argument. Basically, anything and everything passed in this argument
slot is passed unconstrained.</p>

<pre><code>with(\Mockery::type('resource')) OR with(resourceValue()) OR with(typeOf('resource'))
</code></pre>

<p>Matches any resource, i.e. returns true from an is<em>resource() call. The Type
matcher accepts any string which can be attached to "is</em>" to form a valid
type check. For example, \Mockery::type('float') or Hamcrest's floatValue() and
typeOf('float') checks using is_float(), and \Mockery::type('callable') or Hamcrest's
callable() uses is_callable().</p>

<p>The Type matcher also accepts a class or interface name to be used in an instanceof
evaluation of the actual argument (similarly Hamcrest uses anInstanceOf()).</p>

<p>You may find a full list of the available type checkers at
<a href="http://www.php.net/manual/en/ref.var.php">http://www.php.net/manual/en/ref.var.php</a> or browse Hamcrest's function list at
<a href="http://code.google.com/p/hamcrest/source/browse/trunk/hamcrest-php/hamcrest/Hamcrest.php">http://code.google.com/p/hamcrest/source/browse/trunk/hamcrest-php/hamcrest/Hamcrest.php</a>.</p>

<pre><code>with(\Mockery::on(closure))
</code></pre>

<p>The On matcher accepts a closure (anonymous function) to which the actual argument
will be passed. If the closure evaluates to (i.e. returns) boolean TRUE then
the argument is assumed to have matched the expectation. This is invaluable
where your argument expectation is a bit too complex for or simply not
implemented in the current default matchers.</p>

<p>There is no Hamcrest version of this functionality.</p>

<pre><code>with('/^foo/') OR with(matchesPattern('/^foo/'))
</code></pre>

<p>The argument declarator also assumes any given string may be a regular
expression to be used against actual arguments when matching. The regex option
is only used when a) there is no === or == match and b) when the regex
is verified to be a valid regex (i.e. does not return false from preg_match()).
If the regex detection doesn't suit your tastes, Hamcrest offers the more
explicit matchesPattern() function.</p>

<pre><code>with(\Mockery::ducktype('foo', 'bar'))
</code></pre>

<p>The Ducktype matcher is an alternative to matching by class type. It simply
matches any argument which is an object containing the provided list
of methods to call.</p>

<p>There is no Hamcrest version of this functionality.</p>

<pre><code>with(\Mockery::mustBe(2)) OR with(identicalTo(2))
</code></pre>

<p>The MustBe matcher is more strict than the default argument matcher. The default
matcher allows for PHP type casting, but the MustBe matcher also verifies that
the argument must be of the same type as the expected value. Thus by default,
the argument '2' matches the actual argument 2 (integer) but the MustBe matcher
would fail in the same situation since the expected argument was a string and
instead we got an integer.</p>

<p>Note: Objects are not subject to an identical comparison using this matcher
since PHP would fail the comparison if both objects were not the exact same
instance. This is a hindrance when objects are generated prior to being
returned, since an identical match just would never be possible.</p>

<pre><code>with(\Mockery::not(2)) OR with(not(2))
</code></pre>

<p>The Not matcher matches any argument which is not equal or identical to the
matcher's parameter.</p>

<pre><code>with(\Mockery::anyOf(1, 2)) OR with(anyOf(1,2))
</code></pre>

<p>Matches any argument which equals any one of the given parameters.</p>

<pre><code>with(\Mockery::notAnyof(1, 2))
</code></pre>

<p>Matches any argument which is not equal or identical to any of the given
parameters.</p>

<p>There is no Hamcrest version of this functionality.</p>

<pre><code>with(\Mockery::subset(array(0=&gt;'foo')))
</code></pre>

<p>Matches any argument which is any array containing the given array subset. This
enforces both key naming and values, i.e. both the key and value of each
actual element is compared.</p>

<p>There is no Hamcrest version of this functionality, though Hamcrest can check a
single entry using hasEntry() or hasKeyValuePair().</p>

<pre><code>with(\Mockery::contains(value1, value2))
</code></pre>

<p>Matches any argument which is an array containing the listed values. The naming
of keys is ignored.</p>

<pre><code>with(\Mockery::hasKey(key));
</code></pre>

<p>Matches any argument which is an array containing the given key name.</p>

<pre><code>with(\Mockery::hasValue(value));
</code></pre>

<p>Matches any argument which is an array containing the given value.</p>

<h2>Creating Partial Mocks</h2>

<p>Partial mocks are useful when you only need to mock several methods of an object
leaving the remainder free to respond to calls normally (i.e. as implemented).</p>

<p>Unlike other mock objects, a Mockery partial mock has a real concrete object
at its heart. This approach to partial mocks is intended to bypass a number
of troublesome issues with partials. For example, partials might require
constructor parameters and other setup/injection tasks prior to use. Trying
to perform this automatically via Mockery is not a tenth as intuitive as just
doing it normally - and then passing the object into Mockery.</p>

<p>Partial mocks are therefore constructed as a Proxy with an embedded real object.
The Proxy itself inherits the type of the embedded object (type safety) and
it otherwise behaves like any other Mockery-based mock object, allowing you to
dynamically define expectations. This flexibility means there's little
upfront defining (besides setting up the real object) and you can set defaults,
expectations and ordering on the fly.</p>

<h2>Default Mock Expectations</h2>

<p>Often in unit testing, we end up with sets of tests which use the same object
dependency over and over again. Rather than mocking this class/object within
every single unit test (requiring a mountain of duplicate code), we can instead
define reusable default mocks within the test case's setup() method. This even
works where unit tests use varying expectations on the same or similar mock
object.</p>

<p>How this works, is that you can define mocks with default expectations. Then,
in a later unit test, you can add or fine-tune expectations for that
specific test. Any expectation can be set as a default using the byDefault()
declaration.</p>

<h2>Mocking Public Properties</h2>

<p>Mockery allows you to mock properties is several ways. The simplest is that
you can simply set a public property and value on any mock object. The second
is that you can use the expectation methods set() and andSet() to set property
values if that expectation is ever met.</p>

<p>You should note that, in general, Mockery does not support mocking any magic
methods since these are generally not considered a public API (and besides they
are a PITA to differentiate when you badly need them for mocking!). So please
mock virtual properties (those relying on __get and __set) as if they were
actually declared on the class.</p>

<h2>Mocking Public Static Methods</h2>

<p>Static methods are not called on real objects, so normal mock objects can't mock
them. Mockery supports class aliased mocks, mocks representing a class name which
would normally be loaded (via autoloading or a require statement) in the system
under test. These aliases block that loading (unless via a require statement - so please
use autoloading!) and allow Mockery to intercept static method calls and add
expectations for them.</p>

<h2>Generating Mock Objects Upon Instantiation (Instance Mocking)</h2>

<p>Instance mocking means that a statement like:</p>

<p>$obj = new \MyNamespace\Foo;</p>

<p>...will actually generate a mock object. This is done by replacing the real class
with an instance mock (similar to an alias mock), as with mocking public methods.
The alias will import its
expectations from the original mock of that type (note that the original is never
verified and should be ignored after its expectations are setup). This lets you
intercept instantiation where you can't simply inject a replacement object.</p>

<p>As before, this does not prevent a require statement from including the real
class and triggering a fatal PHP error. It's intended for use where autoloading
is the primary class loading mechanism.</p>

<h2>Preserving Pass-By-Reference Method Parameter Behaviour</h2>

<p>PHP Class method may accept parameters by reference. In this case, changes made
to the parameter (a reference to the original variable passed to the method) are
reflected in the original variable. A simple example:</p>

<pre><code>class Foo {
    public function bar(&amp;$a) {
        $a++;
    }
}

$baz = 1;
$foo = new Foo;
$foo-&gt;bar($baz);

echo $baz; // will echo the integer 2
</code></pre>

<p>In the example above, the variable $baz is passed by reference to Foo::bar()
(notice the "&amp;" symbol in front of the parameter?).
Any change bar() makes to the parameter reference is reflected in the original
variable, $baz.</p>

<p>Mockery 0.7+ handles references correctly for all methods where it can analyse the
parameter (using Reflection) to see if it is passed by reference. To mock how a
reference is manipulated by the class method, you can use a closure argument
matcher to manipulate it, i.e. \Mockery::on() - see Argument Validation section
above.</p>

<p>There is an exception for internal PHP classes where Mockery cannot analyse
method parameters using Reflection (a limitation in PHP). To work around this,
you can explicitly declare method parameters for an internal class using
/Mockery/Configuration::setInternalClassMethodParamMap().</p>

<p>Here's an example using MongoCollection::insert(). MongoCollection is an internal
class offered by the mongo extension from PECL. Its insert() method accepts an array
of data as the first parameter, and an optional options array as the second
parameter. The original data array is updated (i.e. when a insert() pass-by-reference
parameter) to include a new "_id" field. We can mock this behaviour using
a configured parameter map (to tell Mockery to expect a pass by reference parameter)
and a Closure attached to the expected method parameter to be updated.</p>

<p>Here's a PHPUnit unit test verifying that this pass-by-reference behaviour is preserved:</p>

<pre><code>public function testCanOverrideExpectedParametersOfInternalPHPClassesToPreserveRefs()
{
    \Mockery::getConfiguration()-&gt;setInternalClassMethodParamMap(
        'MongoCollection',
        'insert',
        array('&amp;$data', '$options = array()')
    );
    $m = \Mockery::mock('MongoCollection');
    $m-&gt;shouldReceive('insert')-&gt;with(
        \Mockery::on(function(&amp;$data) {
            if (!is_array($data)) return false;
            $data['_id'] = 123;
            return true;
        }),
        \Mockery::any()
    );
    $data = array('a'=&gt;1,'b'=&gt;2);
    $m-&gt;insert($data);
    $this-&gt;assertTrue(isset($data['_id']));
    $this-&gt;assertEquals(123, $data['_id']);
    \Mockery::resetContainer();
}
</code></pre>

<h2>Mocking Demeter Chains And Fluent Interfaces</h2>

<p>Both of these terms refer to the growing practice of invoking statements
similar to:</p>

<pre><code>$object-&gt;foo()-&gt;bar()-&gt;zebra()-&gt;alpha()-&gt;selfDestruct();
</code></pre>

<p>The long chain of method calls isn't necessarily a bad thing, assuming they
each link back to a local object the calling class knows. Just as a fun example,
Mockery's long chains (after the first shouldReceive() method) all call to the
same instance of \Mockery\Expectation. However, sometimes this is not the case
and the chain is constantly crossing object boundaries.</p>

<p>In either case, mocking such a chain can be a horrible task. To make it easier
Mockery support demeter chain mocking. Essentially, we shortcut through the
chain and return a defined value from the final call. For example, let's
assume selfDestruct() returns the string "Ten!" to $object (an instance of
CaptainsConsole). Here's how we could mock it.</p>

<pre><code>$mock = \Mockery::mock('CaptainsConsole');
$mock-&gt;shouldReceive('foo-&gt;bar-&gt;zebra-&gt;alpha-&gt;selfDestruct')-&gt;andReturn('Ten!');
</code></pre>

<p>The above expectation can follow any previously seen format or expectation, except
that the method name is simply the string of all expected chain calls separated
by "-&gt;". Mockery will automatically setup the chain of expected calls with
its final return values, regardless of whatever intermediary object might be
used in the real implementation.</p>

<p>Arguments to all members of the chain (except the final call) are ignored in
this process.</p>

<h2>Mock Object Recording</h2>

<p>In certain cases, you may find that you are testing against an already
established pattern of behaviour, perhaps during refactoring. Rather then hand
crafting mock object expectations for this behaviour, you could instead use
the existing source code to record the interactions a real object undergoes
onto a mock object as expectations - expectations you can then verify against
an alternative or refactored version of the source code.</p>

<p>To record expectations, you need a concrete instance of the class to be mocked.
This can then be used to create a partial mock to which is given the necessary
code to execute the object interactions to be recorded. A simple example is
outline below (we use a closure for passing instructions to the mock).</p>

<p>Here we have a very simple setup, a class (SubjectUser) which uses another class
(Subject) to retrieve some value. We want to record as expectations on our
mock (which will replace Subject later) all the calls and return values of
a Subject instance when interacting with SubjectUser.</p>

<pre><code>class Subject {

    public function execute() {
        return 'executed!';
    }
}

class SubjectUser {

    public function use(Subject $subject) {
        return $subject-&gt;execute();
    }
}
</code></pre>

<p>Here's the test case showing the recording:</p>

<pre><code>class SubjectUserTest extends PHPUnit_Framework_TestCase
{

    public function teardown()
    {
        \Mockery::close();
    }

    public function testSomething()
    {
        $mock = \Mockery::mock(new Subject);
        $mock-&gt;shouldExpect(function ($subject) {
            $user = new SubjectUser;
            $user-&gt;use($subject);
        });

        /**
         * Assume we have a replacement SubjectUser called NewSubjectUser.
         * We want to verify it behaves identically to SubjectUser, i.e.
         * it uses Subject in the exact same way
         */
        $newSubject = new NewSubjectUser;
        $newSubject-&gt;use($mock);
    }

}
</code></pre>

<p>After the \Mockery::close() call in teardown() validates the mock object, we
should have zero exceptions if NewSubjectUser acted on Subject in a similar way
to SubjectUser. By default the order of calls are not enforced, and loose argument
matching is enabled, i.e. arguments may be equal (==) but not necessarily identical
(===).</p>

<p>If you wished to be more strict, for example ensuring the order of calls
and the final call counts were identical, or ensuring arguments are completely
identical, you can invoke the recorder's strict mode from the closure block, e.g.</p>

<pre><code>$mock-&gt;shouldExpect(function ($subject) {
    $subject-&gt;shouldBeStrict();
    $user = new SubjectUser;
    $user-&gt;use($subject);
});
</code></pre>

<h2>Dealing with Final Classes/Methods</h2>

<p>One of the primary restrictions of mock objects in PHP, is that mocking classes
or methods marked final is hard. The final keyword prevents methods so marked
from being replaced in subclasses (subclassing is how mock objects can inherit
the type of the class or object being mocked.</p>

<p>The simplest solution is not to mark classes or methods as final!</p>

<p>However, in a compromise between mocking functionality and type safety, Mockery
does allow creating "proxy mocks" from classes marked final, or from classes with
methods marked final. This offers all the usual mock object goodness but the
resulting mock will not inherit the class type of the object being mocked, i.e.
it will not pass any instanceof comparison.</p>

<p>You can create a proxy mock by passing the instantiated object you wish to mock
into \Mockery::mock(), i.e. Mockery will then generate a Proxy to the real object
and selectively intercept method calls for the purposes of setting and
meeting expectations.</p>

<h2>Mockery Global Configuration</h2>

<p>To allow for a degree of fine-tuning, Mockery utilises a singleton configuration
object to store a small subset of core behaviours. The three currently present
include:</p>

<ul>
<li>Option to allow/disallow the mocking of methods which do not actually exist</li>
<li>Option to allow/disallow the existence of expectations which are never fulfilled (i.e. unused)</li>
<li>Setter/Getter for added a parameter map for internal PHP class methods (Reflection cannot detect these automatically)</li>
</ul><p>By default, the first two behaviours are enabled. Of course, there are situations where
this can lead to unintended consequences. The mocking of non-existent methods
may allow mocks based on real classes/objects to fall out of sync with the
actual implementations, especially when some degree of integration testing (testing
of object wiring) is not being performed. Allowing unfulfilled expectations means
unnecessary mock expectations go unnoticed, cluttering up test code, and
potentially confusing test readers.</p>

<p>You may allow or disallow these behaviours (whether for whole test suites or just
select tests) by using one or both of the following two calls:</p>

<pre><code>\Mockery::getConfiguration()-&gt;allowMockingNonExistentMethods(bool);
\Mockery::getConfiguration()-&gt;allowMockingMethodsUnnecessarily(bool);
</code></pre>

<p>Passing a true allows the behaviour, false disallows it. Both take effect
immediately until switched back. In both cases, if either
behaviour is detected when not allowed, it will result in an Exception being
thrown at that point. Note that disallowing these behaviours should be carefully
considered since they necessarily remove at least some of Mockery's flexibility.</p>

<p>The other two methods are:</p>

<pre><code>\Mockery::getConfiguration()-&gt;setInternalClassMethodParamMap($class, $method, array $paramMap)
\Mockery::getConfiguration()-&gt;getInternalClassMethodParamMap($class, $method)
</code></pre>

<p>These are used to define parameters (i.e. the signature string of each) for the
methods of internal PHP classes (e.g. SPL, or PECL extension classes like
ext/mongo's MongoCollection. Reflection cannot analyse the parameters of internal
classes. Most of the time, you never need to do this. It's mainly needed where an
internal class method uses pass-by-reference for a parameter - you MUST in such
cases ensure the parameter signature includes the "&amp;" symbol correctly as Mockery
won't correctly add it automatically for internal classes.</p>

<h2>Reserved Method Names</h2>

<p>As you may have noticed, Mockery uses a number of methods called directly on
all mock objects, for example shouldReceive(). Such methods are necessary
in order to setup expectations on the given mock, and so they cannot be
implemented on the classes or objects being mocked without creating a method
name collision (reported as a PHP fatal error). The methods reserved by Mockery are:</p>

<ul>
<li>shouldReceive()</li>
<li>shouldBeStrict()</li>
</ul><p>In addition, all mocks utilise a set of added methods and protected properties
which cannot exist on the class or object being mocked. These are far less likely
to cause collisions. All properties are prefixed with "<em>mockery" and all method
names with "mockery</em>".</p>

<h2>PHP Magic Methods</h2>

<p>PHP magic methods which are prefixed with a double underscore, e.g. _set(), pose
a particular problem in mocking and unit testing in general. It is strongly
recommended that unit tests and mock objects do not directly refer to magic
methods. Instead, refer only to the virtual methods and properties these magic
methods simulate.</p>

<p>Following this piece of advice will ensure you are testing the real API of classes
and also ensures there is no conflict should Mockery override these magic methods,
which it will inevitably do in order to support its role in intercepting method
calls and properties.</p>

<h2>Gotchas!</h2>

<p>Mocking objects in PHP has its limitations and gotchas. Some functionality can't
be mocked or can't be mocked YET! If you locate such a circumstance, please please
(pretty please with sugar on top) create a new issue on Github so it can be
documented and resolved where possible. Here is a list to note:</p>

<ol>
<li><p>Classes containing public __wakeup methods can be mocked but the mocked __wakeup
method will perform no actions and cannot have expectations set for it. This is
necessary since Mockery must serialize and unserialize objects to avoid some
__construct() insanity and attempting to mock a __wakeup method as normal leads
to a BadMethodCallException been thrown.</p></li>
<li><p>Classes using non-real methods, i.e. where a method call triggers a __call
method, will throw an exception that the non-real method does not exist unless
you first define at least one expectation (a simple shouldReceive() call would
suffice). This is necessary since there is no other way for Mockery to be
aware of the method name.</p></li>
<li><p>Mockery has two scenarios where real classes are replaced: Instance mocks and
alias mocks. Both will generate PHP fatal errors if the real class is loaded,
usually via a require or include statement. Only use these two mock types where
autoloading is in place and where classes are not explicitly loaded on a per-file
basis using require(), require_once(), etc.</p></li>
<li><p>Internal PHP classes are not entirely capable of being fully analysed using
Reflection. For example, Reflection cannot reveal details of expected parameters
to the methods of such internal classes. As a result, there will be problems
where a method parameter is defined to accept a value by reference (Mockery
cannot detect this condition and will assume a pass by value on scalars and
arrays). If references as internal class method parameters are needed, you
should use the \Mockery\Configuration::setInternalClassMethodParamMap() method.</p></li>
</ol><p>The gotchas noted above are largely down to PHP's architecture and are assumed
to be unavoidable. But - if you figure out a solution (or a better one than what
may exist), let me know!</p>

<h2>Quick Examples</h2>

<p>Create a mock object to return a sequence of values from a set of method calls.</p>

<pre><code>class SimpleTest extends PHPUnit_Framework_TestCase
{

    public function teardown()
    {
        \Mockery::close();
    }

    public function testSimpleMock()
    {
        $mock = \Mockery::mock(array('pi' =&gt; 3.1416, 'e' =&gt; 2.71));
        $this-&gt;assertEquals(3.1416, $mock-&gt;pi());
        $this-&gt;assertEquals(2.71, $mock-&gt;e());
    }

}
</code></pre>

<p>Create a mock object which returns a self-chaining Undefined object for a method
call.</p>

<pre><code>use \Mockery as m;

class UndefinedTest extends PHPUnit_Framework_TestCase
{

    public function teardown()
    {
        m::close();
    }

    public function testUndefinedValues()
    {
        $mock = m::mock('my mock');
        $mock-&gt;shouldReceive('divideBy')-&gt;with(0)-&gt;andReturnUndefined();
        $this-&gt;assertTrue($mock-&gt;divideBy(0) instanceof \Mockery\Undefined);
    }

}
</code></pre>

<p>Creates a mock object which multiple query calls and a single update call</p>

<pre><code>use \Mockery as m;

class DbTest extends PHPUnit_Framework_TestCase
{

    public function teardown()
    {
        m::close();
    }

    public function testDbAdapter()
    {
        $mock = m::mock('db');
        $mock-&gt;shouldReceive('query')-&gt;andReturn(1, 2, 3);
        $mock-&gt;shouldReceive('update')-&gt;with(5)-&gt;andReturn(NULL)-&gt;once();

        // test code here using the mock
    }

}
</code></pre>

<p>Expect all queries to be executed before any updates.</p>

<pre><code>use \Mockery as m;

class DbTest extends PHPUnit_Framework_TestCase
{

    public function teardown()
    {
        m::close();
    }

    public function testQueryAndUpdateOrder()
    {
        $mock = m::mock('db');
        $mock-&gt;shouldReceive('query')-&gt;andReturn(1, 2, 3)-&gt;ordered();
        $mock-&gt;shouldReceive('update')-&gt;andReturn(NULL)-&gt;once()-&gt;ordered();

        // test code here using the mock
    }

}
</code></pre>

<p>Create a mock object where all queries occur after startup, but before finish, and
where queries are expected with several different params.</p>

<pre><code>use \Mockery as m;

class DbTest extends PHPUnit_Framework_TestCase
{

    public function teardown()
    {
        m::close();
    }

    public function testOrderedQueries()
    {
        $db = m::mock('db');
        $db-&gt;shouldReceive('startup')-&gt;once()-&gt;ordered();
        $db-&gt;shouldReceive('query')-&gt;with('CPWR')-&gt;andReturn(12.3)-&gt;once()-&gt;ordered('queries');
        $db-&gt;shouldReceive('query')-&gt;with('MSFT')-&gt;andReturn(10.0)-&gt;once()-&gt;ordered('queries');
        $db-&gt;shouldReceive('query')-&gt;with("/^....$/")-&gt;andReturn(3.3)-&gt;atLeast()-&gt;once()-&gt;ordered('queries');
        $db-&gt;shouldReceive('finish')-&gt;once()-&gt;ordered();

        // test code here using the mock
    }

}
</code></pre></article>
  </div>

          </div>
        </div>
      </div>
    </div>

  </div>

<div class="frame frame-loading large-loading-area" style="display:none;" data-tree-list-url="/padraic/mockery/tree-list/2c5e3244b72d268d8c70935fcceb39b3d84d57db" data-blob-url-prefix="/padraic/mockery/blob/2c5e3244b72d268d8c70935fcceb39b3d84d57db">
  <img src="https://a248.e.akamai.net/assets.github.com/images/spinners/octocat-spinner-64.gif?1329872007" height="64" width="64">
</div>

      </div>
      <div class="context-overlay"></div>
    </div>


      <!-- footer -->
      <div id="footer" >
        
  <div class="upper_footer">
     <div class="container clearfix">

       <!--[if IE]><h4 id="blacktocat_ie">GitHub Links</h4><![endif]-->
       <![if !IE]><h4 id="blacktocat">GitHub Links</h4><![endif]>

       <ul class="footer_nav">
         <h4>GitHub</h4>
         <li><a href="https://github.com/about">About</a></li>
         <li><a href="https://github.com/blog">Blog</a></li>
         <li><a href="https://github.com/features">Features</a></li>
         <li><a href="https://github.com/contact">Contact &amp; Support</a></li>
         <li><a href="https://github.com/training">Training</a></li>
         <li><a href="http://enterprise.github.com/">GitHub Enterprise</a></li>
         <li><a href="http://status.github.com/">Site Status</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Tools</h4>
         <li><a href="http://get.gaug.es/">Gauges: Analyze web traffic</a></li>
         <li><a href="http://speakerdeck.com">Speaker Deck: Presentations</a></li>
         <li><a href="https://gist.github.com">Gist: Code snippets</a></li>
         <li><a href="http://mac.github.com/">GitHub for Mac</a></li>
         <li><a href="http://mobile.github.com/">Issues for iPhone</a></li>
         <li><a href="http://jobs.github.com/">Job Board</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Extras</h4>
         <li><a href="http://shop.github.com/">GitHub Shop</a></li>
         <li><a href="http://octodex.github.com/">The Octodex</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Documentation</h4>
         <li><a href="http://help.github.com/">GitHub Help</a></li>
         <li><a href="http://developer.github.com/">Developer API</a></li>
         <li><a href="http://github.github.com/github-flavored-markdown/">GitHub Flavored Markdown</a></li>
         <li><a href="http://pages.github.com/">GitHub Pages</a></li>
       </ul>

     </div><!-- /.site -->
  </div><!-- /.upper_footer -->

<div class="lower_footer">
  <div class="container clearfix">
    <!--[if IE]><div id="legal_ie"><![endif]-->
    <![if !IE]><div id="legal"><![endif]>
      <ul>
          <li><a href="https://github.com/site/terms">Terms of Service</a></li>
          <li><a href="https://github.com/site/privacy">Privacy</a></li>
          <li><a href="https://github.com/security">Security</a></li>
      </ul>

      <p>&copy; 2012 <span title="0.04158s from fe9.rs.github.com">GitHub</span> Inc. All rights reserved.</p>
    </div><!-- /#legal or /#legal_ie-->

      <div class="sponsor">
        <a href="http://www.rackspace.com" class="logo">
          <img alt="Dedicated Server" height="36" src="https://a248.e.akamai.net/assets.github.com/images/modules/footer/rackspaces_logo.png?1329521039" width="38" />
        </a>
        Powered by the <a href="http://www.rackspace.com ">Dedicated
        Servers</a> and<br/> <a href="http://www.rackspacecloud.com">Cloud
        Computing</a> of Rackspace Hosting<span>&reg;</span>
      </div>
  </div><!-- /.site -->
</div><!-- /.lower_footer -->

      </div><!-- /#footer -->

    

<div id="keyboard_shortcuts_pane" class="instapaper_ignore readability-extra" style="display:none">
  <h2>Keyboard Shortcuts <small><a href="#" class="js-see-all-keyboard-shortcuts">(see all)</a></small></h2>

  <div class="columns threecols">
    <div class="column first">
      <h3>Site wide shortcuts</h3>
      <dl class="keyboard-mappings">
        <dt>s</dt>
        <dd>Focus site search</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>?</dt>
        <dd>Bring up this help dialog</dd>
      </dl>
    </div><!-- /.column.first -->

    <div class="column middle" style='display:none'>
      <h3>Commit list</h3>
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selection down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selection up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>c <em>or</em> o <em>or</em> enter</dt>
        <dd>Open commit</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>y</dt>
        <dd>Expand URL to its canonical form</dd>
      </dl>
    </div><!-- /.column.first -->

    <div class="column last" style='display:none'>
      <h3>Pull request list</h3>
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selection down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selection up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>o <em>or</em> enter</dt>
        <dd>Open issue</dd>
      </dl>
    </div><!-- /.columns.last -->

  </div><!-- /.columns.equacols -->

  <div style='display:none'>
    <div class="rule"></div>

    <h3>Issues</h3>

    <div class="columns threecols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt>j</dt>
          <dd>Move selection down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>k</dt>
          <dd>Move selection up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>x</dt>
          <dd>Toggle selection</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>o <em>or</em> enter</dt>
          <dd>Open issue</dd>
        </dl>
      </div><!-- /.column.first -->
      <div class="column middle">
        <dl class="keyboard-mappings">
          <dt>I</dt>
          <dd>Mark selection as read</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>U</dt>
          <dd>Mark selection as unread</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>e</dt>
          <dd>Close selection</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>y</dt>
          <dd>Remove selection from view</dd>
        </dl>
      </div><!-- /.column.middle -->
      <div class="column last">
        <dl class="keyboard-mappings">
          <dt>c</dt>
          <dd>Create issue</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>l</dt>
          <dd>Create label</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>i</dt>
          <dd>Back to inbox</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>u</dt>
          <dd>Back to issues</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>/</dt>
          <dd>Focus issues search</dd>
        </dl>
      </div>
    </div>
  </div>

  <div style='display:none'>
    <div class="rule"></div>

    <h3>Issues Dashboard</h3>

    <div class="columns threecols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt>j</dt>
          <dd>Move selection down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>k</dt>
          <dd>Move selection up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>o <em>or</em> enter</dt>
          <dd>Open issue</dd>
        </dl>
      </div><!-- /.column.first -->
    </div>
  </div>

  <div style='display:none'>
    <div class="rule"></div>

    <h3>Network Graph</h3>
    <div class="columns equacols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt><span class="badmono">←</span> <em>or</em> h</dt>
          <dd>Scroll left</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">→</span> <em>or</em> l</dt>
          <dd>Scroll right</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">↑</span> <em>or</em> k</dt>
          <dd>Scroll up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">↓</span> <em>or</em> j</dt>
          <dd>Scroll down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>t</dt>
          <dd>Toggle visibility of head labels</dd>
        </dl>
      </div><!-- /.column.first -->
      <div class="column last">
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">←</span> <em>or</em> shift h</dt>
          <dd>Scroll all the way left</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">→</span> <em>or</em> shift l</dt>
          <dd>Scroll all the way right</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">↑</span> <em>or</em> shift k</dt>
          <dd>Scroll all the way up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">↓</span> <em>or</em> shift j</dt>
          <dd>Scroll all the way down</dd>
        </dl>
      </div><!-- /.column.last -->
    </div>
  </div>

  <div >
    <div class="rule"></div>
    <div class="columns threecols">
      <div class="column first" >
        <h3>Source Code Browsing</h3>
        <dl class="keyboard-mappings">
          <dt>t</dt>
          <dd>Activates the file finder</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>l</dt>
          <dd>Jump to line</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>w</dt>
          <dd>Switch branch/tag</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>y</dt>
          <dd>Expand URL to its canonical form</dd>
        </dl>
      </div>
    </div>
  </div>
</div>

    <div id="markdown-help" class="instapaper_ignore readability-extra">
  <h2>Markdown Cheat Sheet</h2>

  <div class="cheatsheet-content">

  <div class="mod">
    <div class="col">
      <h3>Format Text</h3>
      <p>Headers</p>
      <pre>
# This is an &lt;h1&gt; tag
## This is an &lt;h2&gt; tag
###### This is an &lt;h6&gt; tag</pre>
     <p>Text styles</p>
     <pre>
*This text will be italic*
_This will also be italic_
**This text will be bold**
__This will also be bold__

*You **can** combine them*
</pre>
    </div>
    <div class="col">
      <h3>Lists</h3>
      <p>Unordered</p>
      <pre>
* Item 1
* Item 2
  * Item 2a
  * Item 2b</pre>
     <p>Ordered</p>
     <pre>
1. Item 1
2. Item 2
3. Item 3
   * Item 3a
   * Item 3b</pre>
    </div>
    <div class="col">
      <h3>Miscellaneous</h3>
      <p>Images</p>
      <pre>
![GitHub Logo](/images/logo.png)
Format: ![Alt Text](url)
</pre>
     <p>Links</p>
     <pre>
http://github.com - automatic!
[GitHub](http://github.com)</pre>
<p>Blockquotes</p>
     <pre>
As Kanye West said:

> We're living the future so
> the present is our past.
</pre>
    </div>
  </div>
  <div class="rule"></div>

  <h3>Code Examples in Markdown</h3>
  <div class="col">
      <p>Syntax highlighting with <a href="http://github.github.com/github-flavored-markdown/" title="GitHub Flavored Markdown" target="_blank">GFM</a></p>
      <pre>
```javascript
function fancyAlert(arg) {
  if(arg) {
    $.facebox({div:'#foo'})
  }
}
```</pre>
    </div>
    <div class="col">
      <p>Or, indent your code 4 spaces</p>
      <pre>
Here is a Python code example
without syntax highlighting:

    def foo:
      if not bar:
        return true</pre>
    </div>
    <div class="col">
      <p>Inline code for comments</p>
      <pre>
I think you should use an
`&lt;addr&gt;` element here instead.</pre>
    </div>
  </div>

  </div>
</div>


    <div class="ajax-error-message">
      <p><span class="icon"></span> Something went wrong with that request. Please try again. <a href="javascript:;" class="ajax-error-dismiss">Dismiss</a></p>
    </div>

    
    
    
    <span id='server_response_time' data-time='0.04276' data-host='fe9'></span>
  </body>
</html>

