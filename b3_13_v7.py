 
class Tag:
    def __init__(self, tag, klass=None, toplevel=False, is_single=False, **kwargs):
        self.tag = tag
        self.text = "aaa"
        self.attributes = {}
        self.id = ""
        self.src = ""
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value
    
    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(' %s = "%s"'%(attribute, value))
        attrs = " ".join(attrs)
        
        if self.children:
            print("  <{tag}{attrs}>".format(tag=self.tag, attrs = attrs))          
            for child in self.children:
                print("  "+str(child))
            return "  </%s>"%self.tag
        else:
            if self.is_single:
                return "  <{tag}{attrs}>".format(tag=self.tag, attrs = attrs)
            else:
                return "  <{tag}{attrs}>{text}</{tag}>".format(tag=self.tag, attrs = attrs, text=self.text)
 
class HTML(Tag):
    def __init__(self, output):
        self.tag = "html"
        self.output = output
        self.children = []
        lines = []
        
    def __enter__(self):
        return self
    
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if self.output is None:
            print("<%s>"%self.tag)
            for child in self.children:
                print(child)
            print("</%s>"%self.tag)
        else:
            with open(str(self.output), "w") as f:
                f.write("<%s>"%self.tag+"\n")
                for child in self.children:
                    #print(child)
                    f.writelines(str(child)+"\n")
                    f.writelines(str(print(child))+"\n")
                f.write("</%s>"%self.tag+"\n")
               
class TopLevelTag(HTML):
    def __init__(self, tag):
        self.tag = tag
        self.children = []
        self.attributes = {}
        self.text = "OOO"

    def __enter__(self):
        return self
    
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        return self
    
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(" %s = %s"%(attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            print("<{tag}{attrs}>".format(tag=self.tag, attrs = attrs))          
            for child in self.children:
                print(str(child))
            return "</%s>"%self.tag
        else:
            return print("<{tag}{attrs}>{text}</{tag}>".format(tag=self.tag, attrs = attrs, text=self.text))

if __name__ == "__main__":
    #with HTML(output="test.html") as doc:
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text")) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body
        
