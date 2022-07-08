# FOSSFolio

Probably the simplest static site generator in the world! (Yes, inspired from Carlsberg commercials 😜)  

## About FOSSFolio

FOSSFolio is a Free and Open Source Software (FOSS) meant for developers to create their own static websites (mostly portfolios), with fine-grained control.

## Intended Audience

Developers or coding enthusiasts who need a static site (maybe like a blog) with minimal effort.

## Features

* **Fully Hackable(!)**
* Plugins to extend functionalities of basic templates
* Jinja2 templating (under development)
* Intuitive page structure
* Automatic sitemap generation

## Screenshots

Screenshots taken while building a demo site:

<div style="display: flex;">

<img src="https://user-images.githubusercontent.com/76481787/177839709-3dcf07aa-3844-4735-af77-c1320964b234.png" alt="Build Screenshot" width="70%">
<img src="https://user-images.githubusercontent.com/76481787/177840534-aec51e90-ff32-49fd-b963-6361a4d282cc.png" alt="File structure after building" width="20%">
</div>

## Getting started

The main objective of creating FOSSFolio was to avoid the different complexities imposed by other static site generator (like Hugo) that give you a lot of control, but have quite a learning curve. I really love Hugo, but sometimes it requires a lot of changes even to add/change some basic functionalities.

1. Clone this repository
2. Install dependencies with `pip install -r requirements.txt`
3. Navigate to `fossfolio` folder
4. Clear all the files and subfolders in the `assets` and `posts` folder
5. Put your own content in place of those
6. Run `python build.py`
7. The `build` folder will contain the generated static site.

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

## Additional Notes

Since FOSSfolio is based on Python-markdown under the hood, you can use the additional features of Python-markdown, that don't exist in the vanilla Markdown specifications. Some of those features are:

* [**Attribute lists**](https://python-markdown.github.io/extensions/attr_list/) (a lifesaver for good SEO)
* [**Extensions API**](https://python-markdown.github.io/extensions/api/) (supercharged Markdown)

and so on.
