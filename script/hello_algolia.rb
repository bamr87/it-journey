require 'nokogiri'
require 'algolia'

# Connect and authenticate with your Algolia app
client = Algolia::Search::Client.create('SP02Z3YYL4', ENV['ALGOLIA_ADMIN_API_KEY'])

# Initialize your Algolia index
index = client.init_index('dev_it-journey')

# Initialize objectID counter
objectID = 0

# Parse your Jekyll site
Dir.glob("_site/**/*.html") do |file|
    doc = Nokogiri::HTML(File.open(file))

    # Extract the data you want to index
    title = doc.at_css('title').text
    excerpt = doc.at_css('meta[name="description"]')&.attr('content')
    categories = doc.at_css('meta[name="keywords"]')&.attr('content')&.split(',')
    tags = doc.at_css('meta[name="keywords"]')&.attr('content')&.split(',')

    # Parse only the "main-content" div
    main_content = doc.at_css('#main-content')

    # Create one object per heading
    headings = main_content.css('h1, h2, h3, h4, h5, h6')
    headings.each_with_index do |heading, i|
        # Get the content after the heading until the next heading
        content = []
        node = heading.next
        while node && (i == headings.length - 1 || node != headings[i + 1])
            content << node.text if node.name == 'p'
            node = node.next
        end

        record = {
            'objectID': objectID,
            'title': title,
            'excerpt': excerpt,
            'categories': categories,
            'tags': tags,
            'path': file,
            'level': heading.name,
            'text': heading.text,
            'content': content.join(' ')
        }

        # Send the data to your Algolia index
        index.save_object(record).wait()

        # Increment objectID counter
        objectID += 1
    end
end