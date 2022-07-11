# FOSSFolio
<img src="https://user-images.githubusercontent.com/76481787/178124946-03464baa-9493-44a4-93e1-e52e5ef1ad5c.png" alt="Fossfolio Logo" width="50%">

<a href="https://www.producthunt.com/posts/fossfolio?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-fossfolio" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=352081&theme=light" alt="Fossfolio - Probably&#0032;the&#0032;simplest&#0032;static&#0032;site&#0032;generator&#0032;in&#0032;the&#0032;world&#0033; | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

Probably the simplest static site generator in the world! (Yes, inspired from Carlsberg commercials 😜)  

## About FOSSFolio

FOSSFolio is a Free and Open Source Software (FOSS) meant for developers to create their own static websites (mostly portfolios), with fine-grained control.

## Intended Audience

Developers or coding enthusiasts who need a static site (maybe like a blog) with minimal effort.

## Features

* **Fully Hackable(!)**
* **Plugins to extend functionalities of basic templates:** A plugin can be anything- from replacing a simple placeholder with some simple value, to some complex JavaScript embedding beast, you can do anything with plugins, as long as you follow the rules for [Plugin Development](#plugin-development) 
* **Jinja2 templating (under development):** You can use Jinja templating for all your themes, as well as create themes based on it!
* **Flexible page structure:** Whatever page structure you want, you can have it 😃, as long as you place it inside the `content/` folder, directly or indirectly. You just need to have a theme for it (or customize your theme accordingly).
* **Automatic sitemap generation on-the-fly**: Yes, I know that getting the SEO right is a pain. So I implemented an automated sitemap generator, which generates readable sitemaps (to the best of my knowledge) that can be easily crawled by Search Engine Bots 🥳.

## Screenshots

**Console while building a demo site:**

<div style="display: flex;">
  <img src="https://user-images.githubusercontent.com/76481787/177839709-3dcf07aa-3844-4735-af77-c1320964b234.png" alt="Build Screenshot" width="70%">
  <img src="https://user-images.githubusercontent.com/76481787/177840534-aec51e90-ff32-49fd-b963-6361a4d282cc.png" alt="File structure after building" width="20%">
</div>
<br><br>

**Post rendered with default theme using the `default.html` mapping:**

<div style="display: flex;">
  <img src="https://user-images.githubusercontent.com/76481787/178124033-3f7b2b26-5c44-4ab1-b149-e7ca37aca1cc.png" alt="Sample page wrapped in default theme">
</div>
<br><br>

**Example of an auto-generated sitemap**:

<div style="display: flex;">
  <img src="https://user-images.githubusercontent.com/76481787/178124342-cee1f96a-9bbf-4039-9258-614b02774d3d.png" alt="Auto-generated sitemap example">
</div>

## Getting started

The main objective of creating FOSSFolio was to avoid the different complexities imposed by other static site generator (like Hugo) that give you a lot of control, but have quite a learning curve. I really love Hugo, but sometimes it requires a lot of changes even to add/change some basic functionalities.

1. Clone this repository
2. Open the folder.
3. Install poetry using `pip install --upgrade poetry`.
4. Initialize poetry with `poetry init`
5. Install dependencies with `poetry install`
6. Navigate to `fossfolio` folder
7. Clear all the files and subfolders in the `assets` and `posts` folder
8. Put your own content in place of those
9. Run `python build.py`
10. The `build` folder will contain the generated static site.

## Templating with FOSSFolio

There are two kinds of syntaxes for templating with FOSSFolio:

* Plugin templates
* Jinja templates (coming soon)

### Plugin Templates

Plugins are the ad-hoc extensions in FOSSFolio. Plugin templates and their syntax are decided by the devs who write them - You have full control here!

#### Default Plugins:

I've given two default plugins for now:
* The `date_time` plugin: Inserts the current date-time wherever you insert `<% current_time %>` in your markdown files (Inspired from EJS syntax 😃)

* The `user_metadata` plugin: Inserts your PC's hostname wherever you insert `<% user %>` in your markdown files. 

### Jinja templates *(Under devlopment)*

You can use Jinja templates too. The context passing mechanism is under development.
## Hacking around

Keeping the intended audience in mind, the USP of FOSSFolio is the degree of customization it offers. You can hack about just anything - the templates, the plugins - heck even the `build.py` is a small file that aggregates all the small modules into a default workflow - you can hack around that as well.

You can even integrate the modules and functionalities into other larger programs!

<h2 id="plugin-developmenr">Plugin Development</h2>

A plugin can consist of anything, as long as it satisfies the following criteria:

1. It has to act like a module (that is, it should have an `__init__.py`)
2. It should have a `main.py` file that acts like a controller for other functionalities of the plugin.
3. It should have a `run` method inside `main.py`, that will act as the controller method
4. The `run` method should return a string containing the modified html code. (Be very careful at this step, since it may open your plugin to JS-based vulnerabilities. Any sanity checks are your responsibility - in exchange for maximum freedom with what you can do.) 

**Some points you may want to keep in mind:**

1. Plugins are processed before wrapping the html code in the template. So you should be careful not to change any placeholder for Jinja while processing.
2. Not a strict rule, but `<%...%>` style is pretty familiar to most developers around the world (thanks to JSP, EJS, etc). So you may want to keep placeholders in that format for better readability.

## Additional Notes

Since FOSSfolio is based on Python-markdown under the hood, you can use the additional features of Python-markdown, that don't exist in the vanilla Markdown specifications. Some of those features are:

* [**Attribute lists**](https://python-markdown.github.io/extensions/attr_list/) (a lifesaver for good SEO)
* [**Tables**](https://python-markdown.github.io/extensions/tables/) (to create tables in Markdown that will be rendered to HTML) 

and so on.

For more extensions, you can check out the [**Extensions Glossary**](https://python-markdown.github.io/extensions/) to supercharge Markdown!
