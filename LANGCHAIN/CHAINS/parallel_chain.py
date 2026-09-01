from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel #with help of this we can execute multiple chains parallelly
load_dotenv()

model1=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
model2=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt1=PromptTemplate(
    template='Generate a short and simple notes from the following text \n {text} ',
    input_variables=['text']
)

prompt2=PromptTemplate(
    template='generate 5 short answer questions from the following text \n {text} ',
    input_variables=['text']
)

prompt3 = PromptTemplate(
    template = 'Merge the provided notes and quiz into a single document \n {notes} and {quiz}',
    input_variables=['notes','quiz']
)

parser=StrOutputParser()

#parallel chain

parallel_chain = RunnableParallel(
    {'notes':prompt1 | model1 | parser,
    'quiz': prompt2 | model1 | parser
    }
)

merge_chain = prompt3 | model1 | parser

chain= parallel_chain | merge_chain

text='''The 2017 paper Attention Is All You Need introduced the Transformer architecture, the breakthrough behind modern AI systems like ChatGPT, Claude, and Gemini. By replacing slow sequential processing with attention mechanisms, Transformers made AI faster, more parallelizable, and far better at understanding language, images, and documents.

Key Takeaways:

Transformers process all words at once, not one by one, enabling much faster and more accurate AI.
The attention mechanism helps AI understand context and relationships across entire inputs simultaneously.
The same Transformer architecture that powers chatbots also drives Vision AI and document processing tools like Parseur.
The 2017 Paper That Made ChatGPT Possible
In 2017, a team of eight researchers at Google published a research paper with a bold title: "Attention Is All You Need." At the time, it sounded almost provocative. Most AI systems still relied on older approaches that processed language step by step, one word at a time.

But this paper introduced something entirely new: the Transformer architecture.

The team, Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin, were all working at Google Brain at the time. Many of them have since gone on to found major AI companies of their own, which gives some sense of the calibre of researchers behind this single paper.

Seven years later, Transformers power nearly every major AI breakthrough we use today, including ChatGPT, Claude, Gemini, DALL-E, Whisper, and the Vision AI systems behind document processing platforms like Parseur.

This single paper changed how machines understand language, images, documents, and even speech.

If you have ever wondered how modern AI tools can summarize text, answer questions, extract invoice data, or understand complex documents, the answer usually starts with Transformers.

In this guide, we explain what problem Transformers solved, how the attention mechanism works in simple terms, why Transformers outperformed older AI architectures, and how Transformers power modern document and Vision AI systems.

No equations. No computer science degree required. Just practical explanations, real-world examples, and a clear look at the breakthrough that became the foundation of modern AI.

How AI Used To Process Language (And Why It Was Slow)
Before the Transformer architecture changed AI, most language models relied on a class of models called Recurrent Neural Networks (RNNs).

RNNs were designed to process language one word at a time, in sequence. That sounds reasonable at first because humans also read sentences in order. But this approach created major limitations that slowed AI progress for years.

Here is a simple example: "The cat sat on the mat."

An RNN would process the sentence like this: read "The," process it, store it in memory, then read "cat," process it, remember "The cat," then read "sat," and so on, continuing word by word until the sentence ends.

Everything happened sequentially. Each new word depended on the previous step finishing first.

That was the core problem.

Modern GPUs are incredibly powerful because they can process many operations simultaneously. But RNNs could not fully take advantage of that power because they forced the model to move through text step by step, like a person slowly reading a sentence with a flashlight.

This created a major speed bottleneck: training AI models took days or even weeks, scaling to larger datasets became extremely expensive, long documents were difficult to process efficiently, and real-time applications were harder to build.

But speed was not the only issue. RNNs also struggled with memory.

Imagine this sentence: "The cat, which was sitting on the mat that my grandmother gave me for my birthday last year, was sleeping."

By the time the model reaches "was sleeping," the important subject, "the cat," is now very far away in the sequence.

This is an example of a long-range dependency. As words get farther apart, RNNs have a harder time preserving the connection between them because information must pass through many sequential steps, which makes distant dependencies harder to learn and maintain.

In practice, this meant older AI systems often lost context in long paragraphs, complex documents, technical writing, conversations, and multi-page files.

The issue became even more obvious in document AI workflows. An invoice number at the top of a page might need to connect to totals near the bottom. A contract clause might reference terms several paragraphs earlier. Sequential models struggled to reliably maintain these relationships.

Researchers tried improving RNNs with newer architectures like LSTMs and GRUs, but the underlying limitation remained the same: language was still being processed sequentially.

That sequential design created a fundamental speed and memory ceiling that modern AI could not scale beyond.

Then, in 2017, the Transformer architecture arrived and changed everything.

What If We Looked At All Words Simultaneously?
The breakthrough behind the Transformer architecture was surprisingly simple: what if AI did not process language word by word at all?

Instead of reading sentences sequentially like older RNN models, Transformers analyze all words simultaneously and determine which words matter most to each other.

This idea became known as the attention mechanism. An attention mechanism is a machine learning technique that directs models to focus on the most relevant parts of the input, which is why it is so important in Transformer-based systems.

To understand how this works, it helps to think about how humans naturally understand context. Take the word "bank." That word can mean very different things depending on the sentence.

"The bank by the river is steep." Here, "bank" connects to "river" and becomes geographic.

"The bank approved my loan." Here, "bank" connects to "loan" and becomes financial.

Humans instantly understand the difference because our brains automatically connect "bank" to nearby contextual clues. The Transformer attention mechanism works similarly.

Instead of treating words independently, the model constantly evaluates relationships between words and decides which connections are most important for understanding meaning. The model assigns higher weight to the words that matter most for the current word or task, rather than giving every word equal importance.

This becomes especially powerful in longer sentences. According to IBM, the attention mechanism "pays attention to the words that matter most for the next translated word," which improves accuracy and handling of long sequences.

Consider: "The cat, which was sitting on the mat, was sleeping."

Older RNN models often struggled here because "cat" and "sleeping" are separated by many words. But Transformers handle this differently.

Using attention, "sleeping" directly attends to "cat," "was" attends to "cat" to understand the subject, and "mat" attends to "sitting" for location context. These connections happen instantly across the entire sentence. Nothing needs to wait for previous words to finish processing.

A useful analogy is highlighting text while reading. When humans read, we naturally focus on the most relevant words: nouns connected to actions, subjects connected to verbs, references connected to earlier context. Your brain does this automatically and almost instantly. Attention gives AI a similar capability.

Here is the key difference in how each approach processes a 100-word sentence:

RNN Processing: Word 1, process, Word 2, process, Word 3, process. Everything happens step by step. A 100-word sentence requires 100 sequential operations.

Transformer Processing: All words, attention analysis, contextual understanding. Everything happens simultaneously. A 100-word sentence can be processed in parallel.

That parallel processing advantage was enormous. Modern GPUs are built to handle thousands of operations at once. Transformers finally allowed AI systems to fully use that hardware power efficiently.

The result was dramatically faster training, better long-context understanding, improved scalability, and stronger performance on language tasks.

This is why Transformers rapidly replaced older architectures across the AI industry. The same attention mechanism now powers language models like ChatGPT, document AI systems, translation tools, speech recognition, Vision AI platforms, and image generation systems.

Breaking Down The Transformer: Four Key Components
The Transformer architecture can sound intimidating at first. But the core ideas are actually surprisingly intuitive once you strip away the technical jargon.

At a high level, Transformers rely on four major components working together: self-attention, multi-head attention, positional encoding, and feed-forward networks. Together, these components allow modern AI systems to understand relationships, context, meaning, and structure far more effectively than older AI architectures.

Component 1: Self-Attention (The Core Innovation)
The most important idea in the Transformer architecture is self-attention.

Self-attention allows every word in a sentence to look at every other word and decide which ones matter most. That is the heart of the attention mechanism.

Imagine the sentence: "The cat sat on the mat."

When processing the word "cat," the model does not look only at nearby words. It evaluates the entire sentence simultaneously. Internally, the Transformer asks three questions for every word.

Query: "What information am I looking for?"

Key: "What kind of information do I offer?"

Value: "What actual information do I carry?"

You can think of it like a matchmaking system between words. For the word "cat," the Query asks what relationships matter, the model compares the query against the Keys of every other word, and strong matches receive closer attention.

So "cat" might strongly attend to "sat" (action relationship) and "mat" (location relationship), and weakly attend to smaller function words like "the" and "on," which still matter but less strongly.

The result is that the model creates a richer understanding of "cat," not as an isolated word, but as "the cat that sat on the mat."

Self-attention solved several major problems at once: every word can directly connect to every other word, long-distance relationships are preserved, processing happens in parallel, and context understanding improves dramatically. This is one of the main reasons Transformers rapidly overtook older RNN architectures.

Component 2: Multi-Head Attention (Multiple Perspectives)
One attention mechanism is powerful. But the researchers realized something important: different types of relationships exist inside language. A single attention layer might focus heavily on grammar but miss meaning. So the Transformer architecture introduced multi-head attention.

Instead of using one attention system, Transformers run multiple attention mechanisms simultaneously. These are called attention heads. You can think of them as multiple specialists analyzing the same sentence from different perspectives.

One head might focus on grammar: subjects, verbs, and sentence structure. Another focuses on semantic meaning: "cat" as an animal, "mat" as an object. Another focuses on position: which words appear earlier or later. Another focuses on references: "it" referring to "cat."

A useful analogy is viewing a painting from multiple angles. One angle reveals color. Another reveals texture. Another reveals depth. Together, those perspectives create a fuller understanding. That is exactly how multi-head attention works.

This layered understanding is a major reason modern AI systems can generate responses that feel coherent, contextual, and surprisingly human-like.

Component 3: Positional Encoding (Preserving Word Order)
There was one major challenge with parallel processing. If Transformers process all words simultaneously, how do they know word order?

Consider: "Dog bites man." and "Man bites dog." These contain the same words but completely different meanings.

This is where positional encoding comes in. Transformers add position information to every word before processing begins. Word 1 receives one positional signal, word 2 receives another, and so on. This allows the model to preserve sequence information while still processing everything in parallel.

A simple analogy is timestamps on photos. Without timestamps, you know what happened but not the order. With timestamps, you can reconstruct the timeline. Positional encoding gives Transformers that same sense of order.

This becomes extremely important for sentence structure, meaning, grammar, chronology, and document layout interpretation. Without positional information, language understanding would quickly break down.

Component 4: Feed-Forward Networks (Refining Understanding)
After attention gathers context, the Transformer still needs to refine and strengthen its understanding. That is the role of the feed-forward network.

You can think of this step as polishing the interpretation. Attention identifies relationships. Feed-forward layers help transform those relationships into richer internal representations. The model repeatedly improves its understanding of what each word represents in context.

This refinement process helps Transformers become better at prediction, reasoning, classification, generation, and summarization. Every layer adds more contextual depth.

The Complete Transformer Architecture Explained
Now let us put everything together.

The original Transformer architecture introduced in "Attention Is All You Need" used an encoder-decoder structure. Each half has a distinct job.

Encoder: Understanding the Input
The encoder's job is to understand incoming text. It receives the input sentence, applies self-attention to understand relationships between all words, applies feed-forward refinement, and repeats the process multiple times. Each layer builds increasingly rich contextual understanding. By the end, the encoder produces deeply contextual representations of the input, capturing not just what each word means, but how it relates to everything around it.

Decoder: Generating the Output
The decoder's job is to generate output text, one token at a time, through a process called auto-regressive decoding. This works differently from the encoder. Where the encoder processes all input simultaneously, the decoder generates output sequentially.

The decoder achieves this through three mechanisms working together.

Masked self-attention: When generating each new word, the decoder can only attend to words it has already generated, not future ones. This masking prevents the model from "cheating" during training by looking ahead at what it is supposed to produce.

Cross-attention: The decoder also attends to the encoder's representations of the input. This is the bridge between understanding and generation. For a translation task, the decoder looks at the full encoded source sentence to decide what word to generate next. For question answering, it attends to the encoded context to produce a relevant answer.

Feed-forward layers: The same refinement step used in the encoder, which deepens the decoder's understanding before generating each token.

In practice, output generation works like this: the decoder starts with a special "begin" token, attends to the encoder output and that token, generates the first output word, then uses that word as new input. It then attends to the encoder output and all previously generated words, generates the next word, and repeats the cycle until a special "end" token is generated.

This is the same fundamental process that powers modern AI systems today. When you ask ChatGPT or Claude a question, a decoder generates each word of the response one at a time, attending to your full prompt plus everything it has generated so far.

The 2017 paper used an encoder-decoder structure specifically for machine translation. Many modern systems, including GPT models, use decoder-only architectures. But the auto-regressive generation principle introduced in the original paper remains central to how large language models work today.

Three Reasons Transformers Beat RNNs
When the Transformer architecture was introduced in Attention Is All You Need, it did not just improve existing AI models. It fundamentally changed how machines process language. Compared to older Recurrent Neural Networks (RNNs), Transformers were faster, more parallelizable, and far better at understanding context.

1. Parallel Processing Makes Transformers Much Faster
Before Transformers, language models processed text one word at a time. With an RNN, each word depended on the previous one finishing first. That created a major speed bottleneck, especially because modern GPUs are designed for parallel processing and could not be fully utilized with sequential models.

Transformers solved this by processing all words simultaneously using the attention mechanism. The result was dramatic. The original paper demonstrated this clearly: earlier RNN-based translation systems often required weeks of training, while the Transformer-based model achieved state-of-the-art results in roughly 12 hours on modern hardware. Training became 10 to 100 times faster, GPUs could be fully utilized, and larger datasets became practical to train on.

This speed improvement is one reason large AI systems like ChatGPT and Gemini became possible.

2. Transformers Understand Long-Range Context Better
RNNs also struggled with long-range dependencies, connecting words that are far apart in a sentence. Consider: "The cat, which had been sitting near the window for most of the afternoon while watching birds outside, was sleeping."

By the time an RNN reaches "was sleeping," the connection to "the cat" has weakened because the information passed through dozens of intermediate words. At each step, some context gets diluted or forgotten.

Transformers use attention to create direct connections between related words. In the sentence above, "sleeping" can directly attend to "cat," "window" can connect to "watching," and "birds" can influence surrounding context instantly. No matter how far apart the words are, the relationship remains strong.

This was a massive breakthrough because language depends heavily on context spread across long passages. It also made Transformers far more effective for long documents, conversations, legal contracts, technical documentation, and Vision AI and document processing. Today's large language models can process thousands, or even hundreds of thousands, of tokens in a single context window because of this architecture.

3. Transformers Scale Extremely Well
The final reason Transformers won is scalability. As AI researchers increased model size, RNNs became increasingly inefficient. Transformers handled scaling much more effectively.

Modern AI systems improve dramatically when you increase training data, model size, context length, and compute power. Transformers were uniquely suited for this. As sequences get longer, RNNs face increasing processing time and memory limitations. Transformers can handle long sequences efficiently, parallelize workloads across GPUs, train on enormous datasets, and support massive parameter counts.

That scalability enabled GPT-4, Claude, DALL-E, modern Vision AI systems, and advanced document understanding tools. It also made AI economically viable at scale.

The original Transformer paper delivered better performance with lower computational cost. For machine translation, the previous best BLEU score was 26.3. The Transformer achieved 28.4, while also being dramatically faster to train and cheaper to run. Better accuracy, faster training, lower cost, and greater scalability: that combination is why the Transformer architecture rapidly replaced RNNs across nearly every major AI field.

From Research Paper To ChatGPT: The Transformer Revolution
The Attention Is All You Need paper did not just improve machine translation. It triggered an AI revolution that completely changed how modern artificial intelligence systems are built.

2018 to 2019: Language Models Explode
The first major wave of Transformer adoption came through large language models.

GPT (OpenAI): OpenAI built GPT using the Transformer decoder architecture introduced in the original paper. The idea was to pre-train a Transformer on massive amounts of internet text, let it learn grammar, facts, reasoning patterns, and context, then fine-tune it for downstream tasks. Each generation scaled larger: GPT-1 at 117 million parameters, GPT-2 at 1.5 billion, GPT-3 at 175 billion.

BERT (Google): Google took a different approach with BERT (Bidirectional Encoder Representations from Transformers). Instead of predicting text forward like GPT, BERT looks at words in both directions simultaneously using Transformer encoders. This massively improved search relevance, question answering, and natural language understanding. Google later confirmed that BERT impacted a significant portion of English search queries, helping Search better understand context and intent.

2020: Transformers Learn to See
Researchers soon realized attention mechanisms could work on images too. This led to the creation of Vision Transformers (ViTs).

Instead of treating an image as pixels processed sequentially, Vision Transformers split the image into small patches, treat each patch like a word, and let patches attend to every other patch. The Transformer then learns spatial relationships, object positioning, visual context, and pattern recognition. Vision Transformers quickly matched and in many cases surpassed traditional computer vision models. Transformers were no longer just for language. They became a universal AI architecture.

2022 to 2024: The ChatGPT Era
Modern AI assistants are all built on Transformer foundations. These systems scaled the original 2017 architecture to extraordinary levels: hundreds of billions of parameters, internet-scale training datasets, massive GPU clusters, and long-context memory windows.

Claude (Anthropic) extended Transformer capabilities with constitutional AI alignment, extremely long context windows, and improved reasoning and document understanding.

Gemini (Google) expanded Transformers into fully multimodal systems that handle text, images, audio, and video, all processed through attention mechanisms.

2023 to Present: The Rise of Multimodal AI
The next major leap was combining multiple data types into one unified model. Systems like GPT-4 Vision, Claude 3.5, and Gemini can now understand text and images together, screenshots, PDFs, diagrams, documents, and charts.

This is possible because Transformers can learn relationships across modalities, not just within text. The attention mechanism now connects text tokens to image patches, visual regions to words, and layout structures to semantic meaning. For example, in an invoice, "ACME Corp" attends to the logo nearby, table rows attend to column headers, totals attend to line item amounts, and dates attend to invoice metadata sections.

This is also how modern Vision AI systems work. Parseur uses Transformer-based Vision AI to process invoices, receipts, forms, and contracts by understanding both text and document layout simultaneously.

How Attention Powers Document AI
Transformers did not just change chatbots and language models. They also transformed how AI processes documents.

Modern business documents are far more than plain text. Invoices, receipts, contracts, forms, and reports contain layers of visual structure that traditional OCR systems often struggle to interpret correctly. Documents include headers and footers, tables and line items, logos, signatures, and stamps, spatial relationships between fields, multi-column layouts, and labels connected to values.

Traditional OCR systems mainly read documents character by character or line by line. They can extract text, but they usually struggle to understand how different elements relate to each other on the page. For a deeper look at this difference, see Vision AI vs OCR.

Transformer-based Vision AI works differently. Instead of processing one section at a time, Transformers analyze the entire document simultaneously. The attention mechanism helps the model understand both the text and the visual structure of the page at the same time. This means the AI can learn which labels belong to which values, how tables are organized, which totals relate to which line items, how headers connect to sections below, and where important fields are located based on the layout.

Real Example: Invoice Processing
Imagine an invoice with a vendor name, invoice number, a line items table with quantities and prices, and a total at the bottom.

A Transformer-based Vision AI model does not just read the words independently. It learns the relationships between them through attention.

Spatial relationships: The model learns that the vendor name near the top is the supplier, the invoice number is an identifier, and the table below contains transactional data. Position and layout become part of the meaning.

Hierarchical structure: Attention helps the AI understand that the "Line Items" heading acts as a section header, table rows belong together, columns define categories like quantity and price, and the "Total" field summarizes the table values.

Validation and cross-checking: The attention mechanism can connect individual line item prices, quantities, and the final total. This allows the system to validate whether the math adds up, whether required fields are present, and whether values are logically connected.

Context understanding: "10" inside the Qty column becomes a quantity. "$100" inside the Price column becomes a monetary value. The surrounding structure provides meaning.

How Parseur Uses Transformer-Based Vision AI
Parseur uses Transformer-based Vision AI models to process complex business documents more intelligently. When users upload invoices, receipts, purchase orders, or contracts, the system analyzes the full document visually, understands layout and structure, extracts key fields automatically, identifies relationships between document elements, and converts unstructured files into clean, structured data.

The same attention mechanism introduced in Attention Is All You Need now powers modern document automation workflows.

What You Need To Remember
The biggest breakthrough introduced in Attention Is All You Need was surprisingly simple: instead of processing words one by one, Transformers process all words simultaneously using attention.

That single shift changed the trajectory of modern AI. Before Transformers, AI models struggled with slow training, memory limitations, and long-range understanding. Transformers solved these problems by allowing every word to directly attend to every other word in a sentence at the same time.

The result was a massive leap forward in both speed and capability: 10 to 100 times faster training through parallel processing, better contextual understanding with direct connections between distant words, improved scalability for long documents and massive datasets, and greater versatility across text, images, audio, and document processing.

This architecture quickly became the foundation for nearly every major AI breakthrough after 2018, directly enabling OpenAI's GPT models and ChatGPT, Anthropic's Claude, Google Gemini, image generation systems like DALL-E and Stable Diffusion, and modern Vision AI and Document AI systems.

At its core, attention is about relationships. The model learns which words matter most, which elements connect, how context changes meaning, and how to process information in parallel. It is a simple concept with an enormous impact.

The same attention mechanism that helps AI understand language also helps Vision AI understand documents. In platforms like Parseur, Transformer-based Vision AI models use attention to connect labels with values, understand tables and layouts, extract structured information, and validate relationships across documents. Whether it is a sentence, an invoice, or a contract, the principle is the same: AI becomes more powerful when it understands relationships, not just text.

The Foundation of Modern AI
When the Google researchers published Attention Is All You Need in 2017, they introduced a new architecture for machine translation research. Today, it powers nearly every major AI system we use.

Transformers became the foundation for language models that write and reason, vision models that analyze images, speech systems that transcribe audio, document AI that extracts structured data, and multimodal AI systems that combine text, images, and audio.

The core innovation was surprisingly simple: replace slow sequential processing with parallel attention. Instead of reading information one step at a time, Transformers learn relationships across entire inputs simultaneously. That change unlocked dramatic improvements in speed, scalability, and contextual understanding, and ultimately made modern AI possible.

And Transformers are still evolving. Researchers are now scaling models to trillions of parameters, extending context windows to millions of tokens, applying Transformers to fields like biology, robotics, and climate science, and building faster and more efficient architectures.

At Parseur, Transformer-based Vision AI helps businesses automatically extract data from invoices, receipts, contracts, and other complex documents. The same attention mechanism that powers ChatGPT also powers modern document processing.

Sign up to Parseur for Free
Try out our powerful document processing tool for free.
Share:

Photo of Neha Gunnoo
Neha Gunnoo
LinkedIn
Growth and Marketing Lead at Parseur

Neha Gunnoo writes about AI, automation, and the future of data extraction. With years of experience in SEO and B2B automation strategy, she's passionate about helping businesses ditch manual data entry and scale faster with the right tools. When she's not digging into content strategy or SEO trends, Neha's likely being bossed around by her cat, or trying to catch up to Parseur's founders on passport stamps.'''
result = chain.invoke({'text':text})
print(result)
chain.get_graph().print_ascii()